# Build the TD101 sign-up page for jcsjournals.com from JC's approved mockup ("JC's Cut", 22 Oct 2026).
#
# What it does, and ONLY this (JC, 25 Oct 2026: "the signup form is what is going to be replaced by
# this, that's it, everything else looks the same"):
#   1. The two mockup forms (hero #enroll, closer .endform) lose their fake inputs, select, checkbox,
#      button and "Mockup" message. In their place goes Spira's real Kartra form tag, exactly:
#      <script src="https://app.kartra.com/optin/cxUIOaN2t7dT"></script>
#      Everything around it stays: heading, subline, two-emails line, fine print, chips, agreement line.
#      <form> becomes <div> so Kartra's own <form> is never nested inside one.
#   2. Mockup scaffolding goes: the "JC's cut / not live / form disabled" tag, the review-notes button,
#      every review note (.rv) and the notes script. The "JC's Journals" bar itself stays.
#   3. Images are embedded as data URIs, because on jcsjournals.com a relative img/ path would resolve
#      against the Carrd domain and break. (Same pattern the live hub uses for its background.)
#   4. Kartra's light default form is restyled to the dark page through its container (Spira's step 6).
#      Kartra's markup is never edited or copied.
#   5. The top-right menu (JC, 25 Oct 2026, evening): the bar reads "JC's Journals | Free resources ->" and the
#      three lines; tapping opens a side panel with Free Resource Library, Free Recipe Book and a Socials button
#      that opens Facebook, YouTube, Instagram and Substack. Its words are the only text this build adds (NAV_TEXT).
#
# Output: td101page/jcj.css, td101page/jcj.html, td101page/jcj.js  (same three names the Carrd loader
# fetches, so going live = copying these three over jcj/ and pushing; nothing to re-paste in Carrd).
#
# Gates run on the in-memory text BEFORE anything is written. The text gate uses an independent
# HTML parse of the source (not the regexes that do the edit) to predict exactly which visible words
# must survive, and refuses unless the output carries exactly those words and no others.
#
# Usage:  py -3.12 tools\build-td101-page.py            build + gates + write
#         py -3.12 tools\build-td101-page.py --selftest prove the gates fail on the raw mockup

import base64, hashlib, re, sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "td101-page" / "jcs-cut-2026-10-22.html"
IMG = ROOT / "src" / "td101-page" / "img"
OUT = ROOT / "td101page"

KARTRA_SRC = "https://app.kartra.com/optin/cxUIOaN2t7dT"
KSLOT = '<div class="kslot"><script src="' + KARTRA_SRC + '"></script></div>'

KARTRA_CSS = r"""
/* Kartra form (Spira's real TD101 form), restyled to this page through the container Kartra builds.
   Kartra's markup is never edited. Its default is a white box, white fields and a light blue button. */
.kslot{min-width:0}
.kslot [class^="kartra_optin_container"],.kslot .kartra_optin_container{font-family:var(--body)!important;color:var(--ink)!important}
.kslot .kartra_optin_wrapper{border:0!important;box-shadow:none!important;background:transparent!important}
.kslot .kartra_optin_bgcolor,.kslot .kartra_optin_bgimage{background:transparent!important}
.kslot .kartra_optin_content_wrapper,.kslot .kartra_optin_content_wrapper_inner{padding-left:0!important;padding-right:0!important}
.kslot .kartra_optin_ti,.kslot .kartra_optin_dropdown-toggle{background:#0d130d!important;color:var(--ink)!important;border:1px solid rgba(244,242,234,.25)!important;border-radius:9px!important;font-family:var(--body)!important;font-size:1.02rem!important;box-shadow:none!important}
.kslot .kartra_optin_ti::placeholder{color:#8f8d84!important;opacity:1}
.kslot .kartra_optin_i,.kslot .kartra_optin_caret,.kslot .kartra_optin_filter-option,.kslot .kartra_optin_bs_placeholder{color:var(--mute)!important}
.kslot .kartra_optin_dropdown-menu{background:var(--panel)!important;border:1px solid var(--line)!important}
.kslot .kartra_optin_dropdown-menu a,.kslot .kartra_optin_dropdown-menu span{color:var(--dim)!important}
.kslot .kartra_optin_dropdown-menu li a:hover,.kslot .kartra_optin_dropdown-menu li a:focus{background:#0d130d!important}
.kslot .kartra-optin-checkbox,.kslot .kartra_optin_tnc-form label,.kslot .kartra_optin_gdpr_wrppr small{color:var(--dim)!important;font-size:.95rem!important}
.kslot .kartra-optin-checkbox a,.kslot .kartra_optin_tnc-form a{color:var(--gold)!important}
.kslot .kartra_optin_asterisk{color:var(--gold)!important}
.kslot .kartra_optin_popover{background:var(--panel)!important;color:var(--dim)!important;border:1px solid var(--line)!important}
.kslot .kartra_optin_submit_btn{background:linear-gradient(45deg,#C7A126,var(--gold-2))!important;color:var(--on-gold)!important;border:0!important;border-radius:10px!important;font-family:var(--display)!important;font-weight:800!important;letter-spacing:1.5px!important;text-transform:uppercase!important;padding:17px 18px!important;height:auto!important;box-shadow:none!important}
.kslot .kartra_optin_submit_btn:hover{filter:brightness(1.07)}
/* Kartra's button reads "Submit". The page's own button read "Enroll me free", so the label is drawn by CSS. */
.kslot .kartra_optin_submit_btn_text{font-size:0!important;color:var(--on-gold)!important}
.kslot .kartra_optin_submit_btn_text::after{content:"Enroll me free \2192";font-size:1.02rem;font-family:var(--display);font-weight:800;letter-spacing:1.5px}
"""

# ---------------------------------------------------------------- top-right menu (JC, 25 Oct 2026, evening)
# "JC's journals. Then there should be a vertical line, and then the next text says free resources, and it has an
# arrow pointing to the right to the little three lines." The panel holds the library, the recipe book and a
# Socials button with his four channels (handles as on the old hub, memory jc-social-handles-changed).
NAV_LINKS = [
    ("https://freelibrary.carrd.co/", "Free Resource Library"),
    ("https://freerecipes.carrd.co/", "Free Recipe Book"),
]
NAV_SOCIALS = [
    ("https://www.facebook.com/jc.ortiz.roman/", "Facebook"),
    ("https://www.youtube.com/@jc_ortiz_roman", "YouTube"),
    ("https://www.instagram.com/jc.ortiz.roman/", "Instagram"),
    ("https://jcortizroman.substack.com/", "Substack"),
]
NAV_TEXT = ["Free resources", "Free resources"] + [t for _, t in NAV_LINKS] + ["Socials"] + [t for _, t in NAV_SOCIALS]

NAV_BAR = "\n".join([
    '<div class="topbar gut">',
    '  <div class="in">',
    '    <span class="brand">JC\'s Journals</span>',
    '    <button class="navbtn" type="button" aria-expanded="false" aria-controls="jcj-menu">',
    '      <span class="navsep" aria-hidden="true"></span>',
    '      <span class="navlabel">Free resources</span>',
    '      <svg class="navarrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>',
    '      <span class="burger" aria-hidden="true"><i></i><i></i><i></i></span>',
    '    </button>',
    '  </div>',
    '</div>',
    '<div class="navscrim" data-navclose></div>',
    '<nav class="navpanel" id="jcj-menu" aria-label="Free resources">',
    '  <div class="navhead">',
    '    <span class="navtitle">Free resources</span>',
    '    <button class="navclose" type="button" aria-label="Close menu" data-navclose>'
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>',
    '  </div>',
] + ['  <a class="navlink" href="%s">%s</a>' % (u, t) for u, t in NAV_LINKS] + [
    '  <button class="navlink navsoc" type="button" aria-expanded="false" aria-controls="jcj-socials">Socials'
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>',
    '  <div class="navsub" id="jcj-socials" hidden>',
] + ['    <a href="%s" target="_blank" rel="noopener">%s</a>' % (u, t) for u, t in NAV_SOCIALS] + [
    '  </div>',
    '</nav>',
])

NAV_CSS = r"""
/* top-right menu (JC, 25 Oct 2026): "JC's Journals | Free resources ->" + three lines, side panel on tap */
.topbar .in{flex-wrap:nowrap}
.navbtn{display:flex;align-items:center;gap:10px;background:none;border:0;margin:0;padding:6px 0;color:var(--ink);cursor:pointer;font:inherit;-webkit-tap-highlight-color:transparent;min-width:0}
.navsep{width:1px;align-self:stretch;min-height:24px;background:rgba(244,242,234,.35);flex:none}
.navlabel{font-family:var(--display);font-weight:800;font-size:.74rem;letter-spacing:1.6px;text-transform:uppercase;color:var(--gold);white-space:nowrap;line-height:1.15;text-align:left}
.navarrow{width:18px;height:18px;fill:none;stroke:var(--gold);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;flex:none}
.burger{display:grid;gap:4px;width:34px;height:34px;place-content:center;border:1px solid rgba(228,190,63,.55);border-radius:8px;flex:none}
.burger i{display:block;width:16px;height:2px;border-radius:2px;background:var(--ink)}
.navbtn:hover .burger{border-color:var(--gold)}
.navbtn:focus-visible,.navclose:focus-visible,.navlink:focus-visible,.navsub a:focus-visible{outline:3px solid var(--gold);outline-offset:3px;border-radius:8px}
.navscrim{position:fixed;inset:0;z-index:80;background:rgba(0,0,0,.55);opacity:0;visibility:hidden;transition:opacity .2s ease,visibility 0s linear .2s}
.navpanel{position:fixed;top:0;right:0;bottom:0;z-index:90;width:min(340px,86vw);overflow-y:auto;background:var(--panel);border-left:3px solid var(--gold);box-shadow:-18px 0 50px rgba(0,0,0,.5);padding:max(14px,env(safe-area-inset-top,0px)) 20px 28px;display:flex;flex-direction:column;gap:10px;transform:translateX(100%);visibility:hidden;transition:transform .25s ease,visibility 0s linear .25s}
.jcj-nav-open .navscrim{opacity:1;visibility:visible;transition:opacity .2s ease}
.jcj-nav-open .navpanel{transform:none;visibility:visible;transition:transform .25s ease}
.navhead{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-bottom:10px;margin-bottom:6px;border-bottom:1px solid var(--line)}
.navtitle{font-family:var(--display);font-weight:800;font-size:.8rem;letter-spacing:2px;text-transform:uppercase;color:var(--gold)}
.navclose{width:42px;height:42px;display:grid;place-items:center;background:none;border:1px solid var(--line);border-radius:8px;color:var(--ink);cursor:pointer;padding:0}
.navclose svg,.navsoc svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;flex:none;transition:transform .2s ease}
.navlink{display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;text-align:left;text-decoration:none;font-family:var(--display);font-weight:800;font-size:.92rem;letter-spacing:1.2px;text-transform:uppercase;color:var(--ink);background:#0d130d;border:1px solid rgba(228,190,63,.35);border-radius:10px;padding:15px 16px;cursor:pointer;margin:0}
.navlink:hover{border-color:var(--gold);color:var(--gold-2)}
.navsoc[aria-expanded="true"] svg{transform:rotate(180deg)}
.navsub{display:grid;gap:4px;margin:0 0 0 10px;padding:2px 0 2px 12px;border-left:2px solid rgba(228,190,63,.35)}
.navsub[hidden]{display:none}
.navsub a{display:block;text-decoration:none;color:var(--dim);font-size:1.05rem;padding:10px;border-radius:8px}
.navsub a:hover{color:var(--gold-2);background:rgba(228,190,63,.08)}
@media (max-width:420px){.topbar .in{gap:8px}.brand{font-size:.8rem;letter-spacing:1.1px}.navbtn{gap:7px}.navlabel{font-size:.64rem;letter-spacing:1px}.navarrow{width:15px;height:15px}.burger{width:32px;height:32px}}
@media (max-width:350px){.brand{font-size:.72rem;letter-spacing:.9px}.navlabel{font-size:.58rem;letter-spacing:.8px}.navbtn{gap:6px}}
@media (prefers-reduced-motion:reduce){.navpanel,.navscrim,.navsoc svg{transition:none!important}}
"""

# MEASURED FAILURE (ledger D574, 2026-10-26 01:20 UTC): section 0 below, the Substack handoff, has never subscribed
# anyone. Six probes plus one real enrollment through JC's Kartra link produced no "New free subscriber"
# notification and no welcome email. Substack answers this blind no-cors POST with its normal success redirect
# whether or not it records the subscriber, so a redirect or a 200 is NOT proof. The only proof is the
# "New free subscriber to JC Ortiz-Roman!" email in JC's Gmail naming the test address. Until a change passes that
# test, new enrollments reach Substack only through the Kartra export and Substack import ("pull my sign-ups").
PAGE_JS = r"""/* TD101 page script for jcsjournals.com. Runs once, after the Carrd loader has put jcj.html into #jcj-page. */

/* 0. Substack handoff (JC, 25 Oct 2026: "let's go the automated route"). The moment Kartra accepts an enrollment,
   this page also subscribes the same email to JC's Substack, exactly the way the old hub box did (Substack's own
   embed posts these fields to /api/v1/free). Kartra's script validates, then calls the form's native submit() and
   the browser navigates to Kartra; submit() fires no event, so the native method is wrapped, and a capture-phase
   submit listener covers the jQuery-trigger path. One handoff per form (data flag). keepalive lets the request
   finish while the page navigates away. Measured 25 Oct 2026: the fetch form of this request returns Substack's
   welcome redirect; a hidden-form POST from another origin returns 503. The visitor's consent is the fine print
   under the form ("and to subscribe to JC's email list"). Kartra's markup is never touched. */
(function(){
  var SUBSTACK='https://jcortizroman.substack.com/api/v1/free?nojs=true';
  var MARK='add_lead/cxUIOaN2t7dT';
  function handoff(form){
    try{
      if(!form||!form.action||form.action.indexOf(MARK)<0)return;
      if(form.getAttribute('data-jcj-handoff')==='1')return;
      var el=form.querySelector('input[name="email"]');
      var email=el?String(el.value||'').trim():'';
      if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))return;
      form.setAttribute('data-jcj-handoff','1');
      var here=location.href.split('#')[0];
      var body=new URLSearchParams({first_url:here,first_referrer:'',current_url:here,current_referrer:'',
        first_session_url:here,first_session_referrer:'',referral_code:'',source:'embed',
        referring_pub_id:'',additional_referring_pub_ids:'',email:email});
      if(window.fetch){fetch(SUBSTACK,{method:'POST',mode:'no-cors',credentials:'omit',keepalive:true,body:body}).catch(function(){});}
    }catch(e){}
  }
  var nativeSubmit=HTMLFormElement.prototype.submit;
  HTMLFormElement.prototype.submit=function(){handoff(this);return nativeSubmit.apply(this,arguments);};
  document.addEventListener('submit',function(e){handoff(e.target);},true);
})();

/* 1. Spira's Kartra form. Script tags that arrive through innerHTML never run, so each Kartra tag is
   re-created as a real script element at the same spot. Kartra then draws its form right after it,
   inside the same .kslot. The page's address (kuid, kref, lid, utm_) is left alone: Kartra reads those
   on load and removes them itself, and that is what credits a sign-up to JC's link. */
(function(){
  var page=document.getElementById('jcj-page');
  if(!page)return;
  var tags=page.querySelectorAll('script[src*="app.kartra.com/optin/"]');
  Array.prototype.forEach.call(tags,function(old){
    var s=document.createElement('script');
    s.src=old.getAttribute('src');
    old.parentNode.insertBefore(s,old);
    old.parentNode.removeChild(old);
  });
})();

/* 2. Carrd hijacks hash navigation, so in-page # links (every "Enroll me free" button points at #enroll)
   scroll via JS instead. preventDefault keeps the hash from ever changing. Same fix the hub uses. */
document.addEventListener('click',function(e){
  if(e.defaultPrevented)return;
  var a=e.target.closest('a[href^="#"]');
  if(!a)return;
  var el=document.getElementById(a.getAttribute('href').slice(1));
  if(!el)return;
  e.preventDefault();
  var y=el.getBoundingClientRect().top+window.scrollY-60;
  window.scrollTo({top:y,behavior:'smooth'});
});

/* 3. Arrival on jcsjournals.com/#enroll: Carrd swallows the native jump and wipes the hash, so the hash
   is read at parse time and the jump is instant. Same fix the hub uses. */
(function(){
  var wanted=(location.hash||'').slice(1);
  function land(id){
    if(!id)return;
    var el=document.getElementById(id);
    if(!el)return;
    var de=document.documentElement,prev=de.style.scrollBehavior;
    de.style.scrollBehavior='auto';
    window.scrollTo(0,el.getBoundingClientRect().top+window.scrollY-60);
    de.style.scrollBehavior=prev;
  }
  function run(){ land(wanted); setTimeout(function(){land(wanted);},350); }
  if(document.readyState==='complete')run();
  else window.addEventListener('load',run);
  window.addEventListener('hashchange',function(){ land((location.hash||'').slice(1)); });
})();

/* 4. Top-right menu (JC, 25 Oct 2026). "Free resources" + the three lines open the side panel; the X, the dark
   backdrop and Escape close it. "Socials" opens and closes its own list of four channels. */
(function(){
  var root=document.documentElement;
  var btn=document.querySelector('#jcj-page .navbtn');
  var panel=document.getElementById('jcj-menu');
  if(!btn||!panel)return;
  function isOpen(){return root.classList.contains('jcj-nav-open');}
  function setOpen(on){
    root.classList.toggle('jcj-nav-open',on);
    btn.setAttribute('aria-expanded',on?'true':'false');
    var target=on?panel.querySelector('.navclose'):btn;
    if(target)try{target.focus({preventScroll:true});}catch(e){}
  }
  btn.addEventListener('click',function(){setOpen(!isOpen());});
  Array.prototype.forEach.call(document.querySelectorAll('#jcj-page [data-navclose]'),function(el){
    el.addEventListener('click',function(){setOpen(false);});
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&isOpen())setOpen(false);});
  var soc=panel.querySelector('.navsoc'),sub=document.getElementById('jcj-socials');
  if(soc&&sub)soc.addEventListener('click',function(){
    var on=soc.getAttribute('aria-expanded')!=='true';
    soc.setAttribute('aria-expanded',on?'true':'false');
    sub.hidden=!on;
  });
})();
"""


def fail(msg):
    raise SystemExit("REFUSED: " + msg)


def one(pattern, text, label, flags=re.S):
    m = list(re.finditer(pattern, text, flags))
    if len(m) != 1:
        fail(f"{label}: expected exactly 1 match, found {len(m)}")
    return m[0]


def sub_exact(text, old, new, label, count=1):
    n = text.count(old)
    if n != count:
        fail(f"{label}: expected {count} occurrence(s) of the anchor, found {n}")
    out = text.replace(old, new)
    if count and old in out and old not in new:
        fail(f"{label}: anchor still present after replace")
    return out


# ---------------------------------------------------------------- text gate (independent parse)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Texts(HTMLParser):
    """Collect visible text nodes. With predict=True, also sort each node into kept/removed using the
    rules of the job (rv notes, mockup tag, notes button, form internals go; everything else stays)."""

    KEEP_IN_FORM = {("h2", None), ("p", "s"), ("p", "two-emails"), ("p", "fine"), ("div", "chips"), ("p", "legal")}

    def __init__(self, predict=False):
        super().__init__(convert_charrefs=True)
        self.stack, self.all, self.kept, self.removed, self.predict = [], [], [], [], predict
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "title"):
            self.skip += 1
        if tag in VOID:
            return
        cls = (dict(attrs).get("class") or "").split()
        self.stack.append((tag, cls))

    def handle_endtag(self, tag):
        if tag in ("script", "style", "title"):
            self.skip -= 1
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if self.skip:
            return
        t = " ".join(data.split())
        if not t:
            return
        self.all.append(t)
        if not self.predict:
            return
        classes = [c for _, cl in self.stack for c in cl]
        if "rv" in classes or "mocktag" in classes or "notes-btn" in classes:
            self.removed.append(t)
            return
        in_form = [i for i, (tg, _) in enumerate(self.stack) if tg == "form"]
        if in_form:
            below = self.stack[in_form[-1] + 1:]
            ok = any((tg, None) in self.KEEP_IN_FORM and tg == "h2" for tg, _ in below) or any(
                (tg, c) in self.KEEP_IN_FORM for tg, cl in below for c in cl)
            (self.kept if ok else self.removed).append(t)
            return
        self.kept.append(t)


def visible(html, predict=False):
    p = Texts(predict)
    p.feed(html)
    p.close()
    return p


# ---------------------------------------------------------------- gates
REQUIRED = [
    (KARTRA_SRC, 2),
    ('<div class="kslot">', 2),
    ('id="enroll"', 1),
    ('class="formcard endform"', 1),
    ('class="two-emails"', 2),
    ('class="fine"', 2),
    ('class="legal"', 1),
    ('class="chips"', 1),
    ("Start Where You<br>Actually Are", 1),
    ("Meet My Teacher, Professor Spira", 1),
    ("That First Summer<br>Relapse City", 1),
    ("Later is where this goes to die.", 1),
    ('<span class="brand">JC\'s Journals</span>', 1),
    ('href="#enroll"', 3),
    ("data:image/jpeg;base64,", 11),
    ('aria-controls="jcj-menu"', 1),
    ('id="jcj-menu"', 1),
    ('aria-controls="jcj-socials"', 1),
    ('id="jcj-socials" hidden', 1),
    ('class="burger"', 1),
    ('class="navsep"', 1),
    ('target="_blank" rel="noopener"', 5),   # the footer's Terms of Use link + the four socials
    ('target="_blank"', 5),
] + [('href="%s"' % u, 1) for u, _ in NAV_LINKS + NAV_SOCIALS]
BANNED = ["<form", 'class="rv"', "mocktag", "notes-btn", "Mockup", "form disabled", "not live",
          "Show review notes", "f1-first", "f2-first", 'src="img/', "formmsg", "<select", "<input",
          "—"]
JS_BANNED = ["replaceState", "location.search", "location.href=", "location.replace"]
JS_REQUIRED = [("https://jcortizroman.substack.com/api/v1/free?nojs=true", 1), ("add_lead/cxUIOaN2t7dT", 1),
               ("keepalive:true", 1), ("data-jcj-handoff", 2), ("HTMLFormElement.prototype.submit", 2),
               ("app.kartra.com/optin/", 1), ("jcj-nav-open", 2), ("getElementById('jcj-menu')", 1),
               ("getElementById('jcj-socials')", 1), ("e.key==='Escape'", 1)]


def control_bytes(s):
    return [(i, hex(ord(c))) for i, c in enumerate(s)
            if (ord(c) < 0x20 and c not in "\t\n\r") or 0x7F <= ord(c) <= 0x9F]


def gate(html, css, js, source_fragment):
    problems = []
    for tok, n in REQUIRED:
        k = html.count(tok)
        if k != n:
            problems.append(f"required {tok[:50]!r}: want {n}, found {k}")
    for tok in BANNED:
        if tok in html:
            problems.append(f"banned {tok[:40]!r} present in html ({html.count(tok)}x)")
    for tok in ["—", ".mocktag", ".notes-btn", ".rv{"]:
        if tok in css:
            problems.append(f"banned {tok!r} present in css")
    for tok in JS_BANNED:
        if tok in js:
            problems.append(f"banned {tok!r} present in js (the address must reach Kartra untouched)")
    for tok, n in JS_REQUIRED:
        if js.count(tok) != n:
            problems.append(f"js required {tok!r}: want {n}, found {js.count(tok)}")
    for name, s in (("html", html), ("css", css), ("js", js)):
        cb = control_bytes(s)
        if cb:
            problems.append(f"{name}: {len(cb)} control bytes, first at {cb[:3]}")
    # images: every data URI must decode to the exact bytes of a source image
    hashes = {hashlib.sha256(p.read_bytes()).hexdigest(): p.name for p in IMG.glob("*.jpg")}
    for m in re.finditer(r'src="data:image/jpeg;base64,([A-Za-z0-9+/=]+)"', html):
        h = hashlib.sha256(base64.b64decode(m.group(1))).hexdigest()
        if h not in hashes:
            problems.append("an embedded image does not match any source image")
    # words: output must carry exactly the predicted surviving text, nothing added, nothing else lost
    pred = visible(source_fragment, predict=True)
    want, got = Counter(pred.kept) + Counter(NAV_TEXT), Counter(visible(html).all)
    lost, added = want - got, got - want
    if lost:
        problems.append(f"{sum(lost.values())} text node(s) LOST that should survive: {list(lost)[:4]}")
    if added:
        problems.append(f"{sum(added.values())} text node(s) ADDED: {list(added)[:4]}")
    return problems, pred


# ---------------------------------------------------------------- build
def authored_fragment(raw):
    a = raw.find("<title>")
    b = raw.rfind("</body>")
    if a < 0 or b < 0:
        fail("could not find the authored page between <title> and </body>")
    return raw[a:b]


def build(frag):
    css_m = one(r"<style>\s*/\* Layout:.*?</style>", frag, "main style block")
    css = css_m.group(0)[len("<style>"):-len("</style>")].strip("\n")
    html = frag[:css_m.start()] + frag[css_m.end():]

    # head-only bits that would land inside <body> on Carrd
    html = re.sub(r"<title>.*?</title>\s*", "", html, count=1, flags=re.S)
    html = sub_exact(html, '<meta name="claude:viewport-fit-sides" content="cover">\n', "", "claude meta")
    # the notes toggle + fake-submit script
    s = one(r"\n<script>\s*\(function\(\)\{\s*var btn=document\.getElementById\('notesBtn'\).*?</script>\s*", html, "notes script")
    html = html[:s.start()] + "\n" + html[s.end():]

    # 2. mockup bar -> plain brand bar
    bar = one(r'<div class="mockbar gut">.*?</div>\s*</div>', html, "mockup bar")
    html = html[:bar.start()] + NAV_BAR + html[bar.end():]
    #    review notes
    n_rv = len(re.findall(r'<div class="rv">.*?</div>', html, re.S))
    if n_rv != 12:
        fail(f"review notes: expected 12, found {n_rv}")
    html = re.sub(r'[ \t]*<div class="rv">.*?</div>\n?', "", html, flags=re.S)

    # 1. the two forms
    def piece(block, pat, label):
        return one(pat, block, label).group(0)

    hero = one(r'<form class="formcard" id="enroll" novalidate>.*?</form>', html, "hero form")
    hb = hero.group(0)
    hero_new = "\n        ".join([
        '<div class="formcard" id="enroll">',
        piece(hb, r"<h2>Enroll free, instant access</h2>", "hero h2"),
        piece(hb, r'<p class="s">.*?</p>', "hero subline"),
        KSLOT,
        piece(hb, r'<p class="two-emails">.*?</p>', "hero two-emails"),
        piece(hb, r'<p class="fine">.*?</p>', "hero fine"),
        piece(hb, r'<div class="chips">.*?</div>', "hero chips"),
    ]) + "\n      </div>"
    html = html[:hero.start()] + hero_new + html[hero.end():]

    end = one(r'<form class="formcard endform" novalidate>.*?</form>', html, "closer form")
    eb = end.group(0)
    end_new = "\n      ".join([
        '<div class="formcard endform">',
        KSLOT,
        piece(eb, r'<p class="two-emails">.*?</p>', "closer two-emails"),
        piece(eb, r'<p class="fine">.*?</p>', "closer fine"),
        piece(eb, r'<p class="legal">.*?</p>', "closer legal"),
    ]) + "\n    </div>"
    html = html[:end.start()] + end_new + html[end.end():]

    # 3. images
    def embed(m):
        p = IMG / m.group(1)
        if not p.is_file():
            fail(f"image missing: {p}")
        return 'src="data:image/jpeg;base64,' + base64.b64encode(p.read_bytes()).decode("ascii") + '"'
    html, n_img = re.subn(r'src="img/([a-z0-9-]+\.jpg)"', embed, html)
    if n_img != 11:
        fail(f"images: expected 11 img refs, embedded {n_img}")

    # CSS: mockup bar -> top bar, drop review-note and notes-button rules, add the Kartra skin
    css = sub_exact(css, "/* mockup bar */", "/* top bar */", "css bar comment")
    css = sub_exact(css, ".mockbar{", ".topbar{", "css bar rule")
    css = sub_exact(css, ".mockbar .in{", ".topbar .in{", "css bar .in rule")
    for rule in [r"^\.mocktag\{[^}]*\}\n", r"^\.mocktag b\{[^}]*\}\n", r"^\.notes-btn\{[^}]*\}\n",
                 r'^\.notes-btn\[aria-pressed="true"\]\{[^}]*\}\n', r"^/\* review tags \*/\n",
                 r"^\.rv\{[^}]*\}\n", r"^\.rv b\{[^}]*\}\n", r"^\.notes-on \.rv\{[^}]*\}\n",
                 r"\n[ \t]+\.mocktag\{display:none\}"]:
        css, k = re.subn(rule, "", css, flags=re.M)
        if k != 1:
            fail(f"css rule {rule!r}: expected 1, removed {k}")
    css = sub_exact(css, ".notes-btn:focus-visible,", "", "css focus list")
    css = css.rstrip() + "\n" + KARTRA_CSS.lstrip("\n") + NAV_CSS.lstrip("\n")
    return html.strip() + "\n", css, PAGE_JS


def main():
    raw = SRC.read_text(encoding="utf-8")
    frag = authored_fragment(raw)

    if "--selftest" in sys.argv:
        problems, _ = gate(frag, "", PAGE_JS, frag)
        print(f"selftest: gate on the RAW mockup reports {len(problems)} problem(s)")
        for p in problems[:30]:
            print("  -", p)
        if not problems:
            fail("selftest: the gate passed the raw mockup, so it cannot tell a mockup from a page")
        print("selftest OK: the gate refuses the mockup")
        return

    html, css, js = build(frag)
    problems, pred = gate(html, css, js, frag)
    if problems:
        for p in problems:
            print("  -", p)
        fail(f"{len(problems)} gate problem(s); nothing written")

    OUT.mkdir(exist_ok=True)
    for name, text in (("jcj.html", html), ("jcj.css", css), ("jcj.js", js)):
        (OUT / name).write_text(text, encoding="utf-8", newline="\n")
    # readback from disk, by a later read, against the same gates
    rb = [(OUT / n).read_text(encoding="utf-8") for n in ("jcj.html", "jcj.css", "jcj.js")]
    problems2, _ = gate(rb[0], rb[1], rb[2], frag)
    if problems2:
        fail("readback from disk failed the gates: " + "; ".join(problems2[:3]))
    removed = Counter(pred.removed)
    print(f"built td101page/: html {len(html):,} chars, css {len(css):,}, js {len(js):,}")
    print(f"text kept: {len(pred.kept)} nodes, all present; text removed by design: {sum(removed.values())} nodes")
    for t, c in sorted(removed.items(), key=lambda x: -x[1]):
        print(f"   removed x{c}: {t[:90]}")
    print("gates: PASS (required tokens, banned tokens, images byte-exact, words exact, 0 control bytes)")


if __name__ == "__main__":
    main()
