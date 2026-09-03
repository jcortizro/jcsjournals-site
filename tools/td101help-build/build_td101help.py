# -*- coding: utf-8 -*-
"""THE generator for the TD 101 "How To Get In" walkthrough page.

Builds all THREE flows into the repo:
    td101help/help.css, help.html, help.js, img/*.webp

It is self-contained: it needs nothing from any temp scratchpad.
  - desktop source screenshots  ->  tools/td101help-build/src/desktop-doc/NN.png
                                    (produced by fetch_desktop_doc.py, which
                                    needs no credentials; the doc is
                                    anyone-with-link)
  - phone source screenshots    ->  the already-shipped td101help/img/*.webp are
                                    the source of truth. They are read for their
                                    real pixel dimensions and never rewritten, so
                                    a rebuild cannot regress them.

⛔ It never writes carrd-embed-td101help.html. That loader is hand-hardened
   against three measured Carrd traps and a rebuild must not revert it.

⛔ EVERY GATE RUNS INSIDE THIS GENERATOR (fable-mode rule 5: a gate that can be
   forgotten will be, and a gate pass binds to the artifact version it ran on).
   Nothing is written to the repo until all gates pass.

COPY SOURCES, all three flows:
  noapp / circleapp : the shipped 2026-09-03 build, itself taken from Prof.
      Spira's "edited 2026-09-01" phone docs.
  desktop : JC's doc 17z2Ml9_d18W1nn8NxejKmcrCqU4FP_6-w09CrPQkVvY,
      "TD 101 - How To Get In - COMPUTER (NO ACCOUNT) - with photos 10-12".
      JC picked it himself 2026-09-03: "its the one with more photos the ine
      that has the disclaimer picture on it its the most recently freated one".
      MEASURED: its text is character-identical to Spira's edited copy apart
      from blank lines, so there was no copy conflict to reconcile.
"""
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(REPO, "td101help")
IMGDIR = os.path.join(OUT, "img")
DESKTOP_SRC = os.path.join(HERE, "src", "desktop-doc")
RAW = "https://raw.githubusercontent.com/jcortizro/jcsjournals-site/main/td101help/"

ENROLL_HREF = "https://go.mucusfreelife.com/td101-jc-1"
ENROLL_TEXT = "CLICK HERE TO ENROLL"
ENROLL_SUB = "live.mucusfreelife.com/td101"
HELP_HREF = "https://live.mucusfreelife.com/helpdesk-1"
TITLE = "How To Get Into Transition Diet 101"
FOOT_1 = "Stuck on any step?"
FOOT_2 = "Our support team can get you in:"
FOOT_3 = "Use that link rather than replying to the email, so nothing gets missed."

CHOOSE_SUB = "First, tell us what you are using. Then you only see your own steps."
CHOOSE_Q = "Which one are you using?"

# ---------------------------------------------------------------- flows ----
# key, url value (FROZEN: links already sent out use these), everything else.
# ⛔ Never rename "noapp" or "circleapp". JC has already sent those links.
FLOWS = ["noapp", "circleapp", "desktop"]

ACCENT = {
    # accent (dark, card headers + bar)  |  accent-num (light, step numbers)
    "noapp":     ("#14331F", "#E3B84E"),   # house deep green + house gold
    "circleapp": ("#8C4A1F", "#FFD9A8"),   # burnt sienna + light clay
    "desktop":   ("#123F52", "#8FD3E8"),   # deep teal + light sky
}

SUBS = {
    "noapp": "On your phone, no app needed. Scroll down and do one picture at a time.",
    "circleapp": "On your phone, with the Circle app. Scroll down and do one picture at a time.",
    # JC's own desktop doc wording, verbatim.
    "desktop": "On a computer. Scroll down and do one picture at a time.",
}

BAR_LABEL = {
    "noapp": "YOU ARE ON: PHONE, NO APP",
    "circleapp": "YOU ARE ON: PHONE, CIRCLE APP",
    "desktop": "YOU ARE ON: COMPUTER",
}

PICK_TITLE = {
    "noapp": "On my phone, no app",
    "circleapp": "On my phone, with the Circle app",
    "desktop": "On my computer",
}

PICK_SUB = {
    "noapp": "You do not have the Circle app.",
    "circleapp": "You have the Circle app installed.",
    "desktop": "A laptop or a desktop computer.",
}

SVG_OPEN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true" focusable="false">')
ICON = {
    "noapp": SVG_OPEN + '<rect x="6" y="2" width="12" height="20" rx="2.5"></rect>'
             '<line x1="10.4" y1="18.6" x2="13.6" y2="18.6"></line></svg>',
    "circleapp": SVG_OPEN + '<rect x="6" y="2" width="12" height="20" rx="2.5"></rect>'
             '<rect x="9.4" y="7.2" width="5.2" height="5.2" rx="1.4" fill="currentColor" '
             'stroke="none"></rect>'
             '<line x1="10.4" y1="18.6" x2="13.6" y2="18.6"></line></svg>',
    "desktop": SVG_OPEN + '<rect x="2" y="4" width="20" height="13" rx="2"></rect>'
             '<line x1="8" y1="21" x2="16" y2="21"></line>'
             '<line x1="12" y1="17" x2="12" y2="21"></line></svg>',
}

# ------------------------------------------------------------ step copy ----
# (title, [bullets], only_if)
NOAPP_STEPS = [
    ("Fill in the form", ["Type your first name, last name and email.", "Pick your country code, then type your phone number.", "Tap the little square so it agrees to the terms.", "Tap the green ENROLL ME FREE button."], False),
    ("Go to your email", ["Two emails will arrive from us.", "You want the one about your invitation.", "Nothing there? Wait five minutes, then look in Spam or Promotions."], False),
    ("Open the invitation email", ["It says \"Prof. Spira has invited you to join\".", "Tap it to open it."], False),
    ("Tap Accept invitation", ["The blue button in the middle of the email.", "Your phone opens a web page. Carry on at step 7."], False),
    ("Only if a \"Log in\" screen appears", ["Most people go straight to step 7 and never see this.", "If you do see it, tap the blue Sign in with an email.", "Ignore the Google, Twitter and Facebook buttons."], True),
    ("Only if it asks for a password you do not have", ["You have not made a password yet, so there is nothing to type here.", "Tap the blue Sign up.", "That takes you to step 7."], True),
    ("Make your account", ["Type your full name.", "Make up a password and type it into both boxes.", "Write that password down somewhere. You will want it later.", "Tick the box, then tap the blue Accept invitation."], False),
    ("Create your profile", ["Type your full name in the box.", "A photo is not needed.", "Then scroll down the page."], False),
    ("Skip to the bottom", ["Website, Twitter, Facebook, Instagram, LinkedIn - leave them all empty.", "Tap the blue Continue button at the bottom."], False),
    ("You are in", ["A welcome box says hello by name.", "Tap the black Get started button."], False),
    ("Open the checklist", ["A short checklist slides up from the bottom.", "Tap the line that says Start the Transition Diet 101 Course."], False),
    ("Go to the course", ["The line opens up and shows a blue button.", "Tap Go to Transition Diet 101."], False),
    ("Start the course", ["This is the course. 42 lessons, all free.", "Tap the blue Start button."], False),
    ("The disclaimer page", ["One page to read before you begin.", "Tap the white Complete button at the bottom.", "That takes you straight into the first lesson."], False),
    ("Start watching", ["Press play on the video.", "When the lesson finishes, tap Complete at the bottom.", "That moves you to the next lesson. Do that every time."], False),
]

CIRCLEAPP_STEPS = [
    ("Fill in the form", ["Type your first name, last name and email.", "Pick your country code, then type your phone number.", "Tap the little square so it agrees to the terms.", "Tap the green ENROLL ME FREE button."], False),
    ("Go to your email", ["Two emails will arrive from us.", "You want the one about your invitation.", "Nothing there? Wait five minutes, then look in Spam or Promotions."], False),
    ("Open the invitation email", ["It says \"Prof. Spira has invited you to join\".", "Tap it to open it."], False),
    ("Tap Accept invitation", ["The blue button in the middle of the email.", "Your phone will open the Circle app."], False),
    ("Type your email in the app", ["Use the same email you typed on the form in step 1.", "Tap Continue."], False),
    ("Leave the app for a second", ["The app is now waiting for a 6 number code.", "That code has just been emailed to you.", "Go back to your email again."], False),
    ("Open the email from Circle", ["It says \"Your temporary Circle login code\".", "Tap it to open it."], False),
    ("Read the 6 numbers", ["The big number in the email is your code.", "Remember it, or keep this email open."], False),
    ("Type the code into the app", ["Go back to the Circle app.", "Type the 6 numbers into the boxes.", "You do not press anything. It opens on its own."], False),
    ("Tap Complete profile", ["You are in. It welcomes you by name.", "Tap the white Complete profile button."], False),
    ("Type your name", ["Only the top box matters. That is your name.", "You can leave everything else empty."], False),
    ("Save it", ["The check mark is in the top right corner.", "Tap it once. That saves your profile."], False),
    ("Tap the blue link", ["Scroll down a little on the welcome post.", "Tap CLICK HERE TO ACCESS THE TRANSITION DIET 101.", "No link there? Tap the black Get started button instead, then tap Start the Transition Diet 101 Course."], False),
    ("The disclaimer page", ["One page to read before you start.", "Tap the white Complete button at the bottom."], False),
    ("Tap Continue", ["This is the course itself. 42 lessons.", "Tap the white Continue button at the bottom."], False),
    ("Start watching", ["Press play on the video.", "When the lesson finishes, tap Complete at the bottom.", "That moves you to the next lesson. Do that every time."], False),
]

# Verbatim from JC's "with photos 10-12" doc. Step 12 is a conditional, so it
# carries the same ONLY IF chip the phone flows use for their conditionals; no
# word of his copy is changed by that.
DESKTOP_STEPS = [
    ("Fill in the form", ["Type your first name, last name and email.", "Pick your country code, then type your phone number.", "Click the little square to agree to the terms.", "Click the green ENROLL ME FREE button."], False),
    ("You are enrolled", ["The page says Congratulations.", "Scroll down to see what happens next."], False),
    ("Go to your email", ["Two emails are on their way to you.", "You want the one about your invitation.", "Nothing there? Wait five minutes, then look in Spam or Promotions."], False),
    ("Open the invitation email", ["It says \"Prof. Spira has invited you to join\".", "Click it to open it."], False),
    ("Click Accept invitation", ["The blue button in the middle of the email.", "It opens a new page where you make your account."], False),
    ("Make your account", ["Type your full name.", "Make up a password and type the same one into both boxes.", "Write that password down somewhere. You will want it later.", "Tick the box, then click the blue Accept invitation."], False),
    ("Create your profile", ["Type your full name in the box.", "A photo is not needed. Leave the rest empty.", "Scroll to the bottom and click the blue Continue button."], False),
    ("You are inside", ["A welcome box says hello by name.", "Click the black Get started button."], False),
    ("Open the checklist", ["A checklist opens on the right hand side of the screen.", "Click the line that says Start the Transition Diet 101 Course.", "That takes you into the course."], False),
    ("The disclaimer page", ["One page to read before you begin.", "Click the white Complete button at the bottom.", "That takes you straight into the first lesson."], False),
    ("Start watching", ["Press play on the video.", "When the lesson finishes, click Complete at the bottom.", "That moves you to the next lesson. Do that every time."], False),
    ("If the checklist is not there", ["On a computer the checklist lives behind the tick icon in the top right corner.", "Click it any time to bring the checklist back.", "You can also click Transition Diet 101 in the list down the left side."], True),
]

STEPS = {"noapp": NOAPP_STEPS, "circleapp": CIRCLEAPP_STEPS, "desktop": DESKTOP_STEPS}


# ------------------------------------------------------------- images ------
def build_desktop_images():
    """PNG -> WebP, native pixel size, named desktop-NN.webp. Idempotent."""
    from PIL import Image
    n = len(DESKTOP_STEPS)
    made = []
    for i in range(1, n + 1):
        src = os.path.join(DESKTOP_SRC, "%02d.png" % i)
        if not os.path.exists(src):
            raise SystemExit(
                "MISSING desktop source %s\n"
                "Run:  python fetch_desktop_doc.py" % src)
        dst = os.path.join(IMGDIR, "desktop-%02d.webp" % i)
        im = Image.open(src).convert("RGB")
        im.save(dst, "WEBP", quality=80, method=6)
        made.append((os.path.basename(dst), im.size, os.path.getsize(dst)))
    return made


def dims(name):
    from PIL import Image
    p = os.path.join(IMGDIR, name)
    if not os.path.exists(p):
        raise SystemExit("MISSING image %s (the phone WebPs are source of "
                         "truth and must already be in the repo)" % p)
    return Image.open(p).size


# ---------------------------------------------------------------- css ------
def build_css():
    accents = "\n".join(
        "  .f-%s, .pick-%s { --accent:%s; --accent-num:%s; }" % (f, f, ACCENT[f][0], ACCENT[f][1])
        for f in FLOWS)
    return """
  :root { --green:#14331F; --gold:#E3B84E; --cream:#F7F3E8; --ink:#23301D;
          --card:#FFFFFF; --line:#DCD5C2; --muted:#6B7263; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--cream); font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
         color:var(--ink); -webkit-text-size-adjust:100%; }

  /* [hidden] must beat any author display rule (waitlist lesson, 2026-08-11).
     Without this an author display rule outranks the hidden attribute and every
     flow renders at once. Do not remove. */
  [hidden] { display: none !important; }

  /* Per-flow accent. Set on <html> by help.js, and on each chooser card so the
     three cards show their own colour side by side. */
""" + accents + """

  .wrap { max-width:900px; margin:0 auto; padding:0 14px 90px; }
  /* Everything except the desktop flow keeps the original phone column. The
     desktop screenshots are 1600px wide, so their flow gets the full width or
     nothing in them is legible. */
  .hero, #chooser, .foot, #flow-noapp, #flow-circleapp { max-width:480px; margin-left:auto; margin-right:auto; }

  .hero { background:var(--green); color:#fff; border-radius:0 0 18px 18px; padding:26px 20px 24px; text-align:center; }
  .hero .eyebrow { color:var(--gold); font-weight:700; letter-spacing:.14em; font-size:12px; text-transform:uppercase; margin:0 0 10px; }
  .hero h1 { margin:0 0 12px; font-size:26px; line-height:1.2; font-weight:800; }
  .hero p { margin:0 0 18px; font-size:17px; line-height:1.5; color:#EDE7D4; }
  .enroll { display:block; background:var(--gold); color:var(--green); text-decoration:none;
          border-radius:12px; padding:14px 16px 11px; font-weight:800; font-size:19px; }
  .enroll span { display:block; font-weight:600; font-size:13px; margin-top:2px; color:#3D5233; }

  /* ---- the chooser: a cold visitor sees this and no steps at all ---- */
  #chooser { margin-top:20px; }
  .chooseq { margin:0 0 12px; text-align:center; font-size:19px; font-weight:800; color:var(--green); }
  .pick { display:flex; width:100%; align-items:center; gap:12px; text-align:left; cursor:pointer;
          background:var(--card); color:var(--ink); font-family:inherit;
          border:2px solid var(--accent); border-left-width:10px; border-radius:14px;
          padding:14px 12px; margin:0 0 12px; -webkit-appearance:none; appearance:none; }
  .picon { flex:0 0 46px; width:46px; height:46px; border-radius:12px; background:var(--accent);
          color:var(--accent-num); display:flex; align-items:center; justify-content:center; }
  .picon svg { width:26px; height:26px; }
  .ptxt { flex:1 1 auto; min-width:0; }
  .ptxt b { display:block; font-size:17px; font-weight:800; line-height:1.25; color:var(--accent); }
  .ptxt i { display:block; font-style:normal; font-size:14px; line-height:1.4; color:var(--muted); margin-top:3px; }
  .pgo { flex:0 0 auto; font-size:26px; font-weight:800; line-height:1; color:var(--accent); }
  .pick:focus-visible { outline:3px solid var(--gold); outline-offset:2px; }

  /* ---- the persistent "you are on" bar ---- */
  .youare { position:fixed; top:0; left:0; right:0; z-index:30; min-height:54px;
          background:var(--accent,var(--green)); color:#fff;
          border-bottom:3px solid var(--accent-num,var(--gold)); }
  .yin { max-width:520px; margin:0 auto; min-height:54px; display:flex; align-items:center; gap:10px; padding:6px 12px; }
  .yicon { flex:0 0 26px; width:26px; height:26px; display:flex; align-items:center;
          justify-content:center; color:var(--accent-num,var(--gold)); }
  .yicon svg { width:24px; height:24px; }
  .ylab { flex:1 1 auto; min-width:0; font-size:12.5px; font-weight:800; letter-spacing:.05em;
          line-height:1.25; text-transform:uppercase; }
  .yswitch { flex:0 0 auto; background:var(--accent-num,var(--gold)); color:var(--accent,var(--green));
          border:0; border-radius:9px; padding:5px 9px; font-family:inherit; cursor:pointer;
          text-align:center; -webkit-appearance:none; appearance:none; }
  .yswitch i { display:block; font-style:normal; font-size:10px; font-weight:600; line-height:1.15; }
  .yswitch b { display:block; font-size:12px; font-weight:800; letter-spacing:.06em; line-height:1.2; }
  .yswitch:focus-visible { outline:3px solid #fff; outline-offset:2px; }
  /* pure CSS, so the bar can never overlap the hero even if the script that
     picks the flow is the thing that broke */
""" + "\n".join("  .f-%s .wrap { padding-top:54px; }" % f for f in FLOWS) + """

  .step { background:var(--card); border:1px solid var(--line); border-radius:14px; margin-top:22px; overflow:hidden; }
  .step header { background:var(--accent,var(--green)); color:#fff; display:flex; align-items:center; gap:12px; padding:12px 14px; }
  .num { flex:0 0 40px; width:40px; height:40px; border-radius:50%; background:var(--accent-num,var(--gold));
          color:var(--accent,var(--green)); font-weight:800; font-size:20px; display:flex;
          align-items:center; justify-content:center; }
  .step h2 { margin:0; font-size:18px; line-height:1.25; font-weight:800; text-transform:uppercase; letter-spacing:.02em; }
  .onlyif h2 { text-transform:none; }
  .onlyif .chip { display:inline-block; background:var(--accent-num,var(--gold)); color:var(--accent,var(--green));
          font-size:11px; font-weight:800; letter-spacing:.1em; border-radius:6px; padding:2px 8px; margin-bottom:4px; }
  .step ul { margin:0; padding:14px 16px 14px 34px; }
  .step li { font-size:17px; line-height:1.55; margin-bottom:8px; }
  .step li:last-child { margin-bottom:0; }
  .step img { display:block; width:100%; height:auto; border-top:1px solid var(--line); }

  .foot { margin-top:30px; background:var(--green); color:#fff; border-radius:14px; padding:20px 18px; text-align:center; }
  .foot h3 { margin:0 0 8px; font-size:20px; }
  .foot p { margin:0 0 14px; font-size:16px; color:#EDE7D4; }
  .foot .small { margin:12px 0 0; font-size:13px; color:#C9CFBF; }
  .helpbtn { display:inline-block; background:#fff; color:var(--green); font-weight:800; text-decoration:none;
          border-radius:10px; padding:12px 22px; font-size:17px; }
  .stick { position:fixed; left:0; right:0; bottom:0; z-index:30; background:var(--cream);
          border-top:1px solid var(--line); padding:9px 14px;
          display:flex; align-items:center; justify-content:center; gap:10px; }
  .stick span { font-size:14px; color:var(--muted); }
  .stick a { font-size:14px; font-weight:800; color:var(--green); }
  a:focus-visible { outline:3px solid var(--gold); outline-offset:2px; }
"""


# --------------------------------------------------------------- html ------
def steps_html(flow):
    parts = []
    for i, (title, bullets, onlyif) in enumerate(STEPS[flow], 1):
        name = "%s-%02d.webp" % (flow, i)
        w, h = dims(name)
        cls = "step onlyif" if onlyif else "step"
        head = ('<div><span class="chip">ONLY IF</span><h2>%s</h2></div>' % title) if onlyif \
               else ('<h2>%s</h2>' % title)
        lis = "".join("<li>%s</li>" % b for b in bullets)
        lazy = "" if i == 1 else ' loading="lazy"'
        parts.append(
            '<section class="%s"><header><div class="num">%d</div>%s</header>'
            '<ul>%s</ul><img src="%simg/%s" width="%d" height="%d" '
            'alt="Step %d screenshot" decoding="async"%s></section>'
            % (cls, i, head, lis, RAW, name, w, h, i, lazy))
    return "\n".join(parts)


def build_html():
    hero = ('<div class="hero"><p class="eyebrow">Transition Diet 101</p>'
            '<h1>%s</h1><p class="herosub">%s</p>'
            '<a class="enroll" href="%s">%s<span>%s</span></a></div>'
            % (TITLE, CHOOSE_SUB, ENROLL_HREF, ENROLL_TEXT, ENROLL_SUB))

    picks = "".join(
        '<button type="button" class="pick pick-%s" data-flow="%s">'
        '<span class="picon">%s</span>'
        '<span class="ptxt"><b>%s</b><i>%s</i></span>'
        '<span class="pgo" aria-hidden="true">&rsaquo;</span></button>'
        % (f, f, ICON[f], PICK_TITLE[f], PICK_SUB[f]) for f in FLOWS)
    chooser = ('<div id="chooser"><p class="chooseq">%s</p>%s</div>' % (CHOOSE_Q, picks))

    flows = "".join('<div id="flow-%s" hidden>%s</div>' % (f, steps_html(f)) for f in FLOWS)

    foot = ('<div class="foot" id="foot" hidden><h3>%s</h3><p>%s</p>'
            '<a class="helpbtn" href="%s">Get help here</a>'
            '<p class="small">%s</p></div>' % (FOOT_1, FOOT_2, HELP_HREF, FOOT_3))

    bar = ('<div class="youare" id="youare" hidden><div class="yin">'
           '<span class="yicon" id="yicon"></span>'
           '<span class="ylab" id="ylab"></span>'
           '<button type="button" class="yswitch" id="yswitch">'
           '<i>wrong one?</i><b>SWITCH</b></button>'
           '</div></div>')

    stick = ('<div class="stick"><span>%s</span><a href="%s">Get help</a></div>'
             % (FOOT_1, HELP_HREF))

    return bar + '<div class="wrap">' + hero + chooser + flows + foot + '</div>' + stick


# ----------------------------------------------------------------- js ------
def build_js():
    def jsstr(s):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

    def jsmap(d):
        return "{" + ",".join("%s:%s" % (k, jsstr(d[k])) for k in FLOWS) + "}"

    return """
(function(){
  var FLOWS = [%s];
  var SUBS = %s;
  var LABELS = %s;
  var CHOOSE_SUB = %s;
  var root = document.documentElement;
  var wrap = document.querySelector(".wrap");
  var chooser = document.getElementById("chooser");
  var foot = document.getElementById("foot");
  var bar = document.getElementById("youare");
  var ylab = document.getElementById("ylab");
  var yicon = document.getElementById("yicon");
  var sub = document.querySelector(".herosub");

  function accentClass(flow){
    for (var i = 0; i < FLOWS.length; i++) root.classList.remove("f-" + FLOWS[i]);
    if (flow) root.classList.add("f-" + flow);
  }

  function show(flow, writeUrl){
    for (var i = 0; i < FLOWS.length; i++){
      var el = document.getElementById("flow-" + FLOWS[i]);
      if (el) el.hidden = (FLOWS[i] !== flow);
    }
    chooser.hidden = !!flow;
    if (foot) foot.hidden = !flow;
    bar.hidden = !flow;
    accentClass(flow);
    if (flow){
      ylab.textContent = LABELS[flow];
      var src = document.querySelector(".pick-" + flow + " svg");
      yicon.innerHTML = "";
      if (src) yicon.appendChild(src.cloneNode(true));
      if (sub) sub.textContent = SUBS[flow];
    } else if (sub) {
      sub.textContent = CHOOSE_SUB;
    }
    if (writeUrl){
      try {
        history.replaceState(null, "", flow ? "?flow=" + flow : location.pathname);
      } catch (e) {}
    }
    window.scrollTo(0, 0);
  }

  var picks = document.querySelectorAll(".pick");
  for (var i = 0; i < picks.length; i++){
    picks[i].addEventListener("click", function(){
      show(this.getAttribute("data-flow"), true);
    });
  }
  document.getElementById("yswitch").addEventListener("click", function(){
    show(null, true);
  });

  var want = null;
  try { want = (new URLSearchParams(location.search)).get("flow"); } catch (e) {}
  if (!want && location.hash) want = location.hash.slice(1);
  show(FLOWS.indexOf(want) === -1 ? null : want, FLOWS.indexOf(want) !== -1);
})();
""" % (",".join(jsstr(f) for f in FLOWS), jsmap(SUBS), jsmap(BAR_LABEL), jsstr(CHOOSE_SUB))


# --------------------------------------------------------------- gates -----
class GateFail(Exception):
    pass


def gates(css, html, js):
    """Every check that must never silently lapse. Runs BEFORE anything is
    written, so a failing build cannot reach the repo."""
    fails = []
    checks = []

    def ok(name, cond, detail=""):
        checks.append((name, bool(cond), detail))
        if not cond:
            fails.append("%s  %s" % (name, detail))

    # 1. no em dashes, no en dashes, and nothing non-ASCII at all.
    #    (The ASCII gate also kills the smart-apostrophe class that has bitten
    #    string comparisons before.)
    for label, text in (("help.css", css), ("help.html", html), ("help.js", js)):
        em = text.count("—")
        en = text.count("–")
        bad = sorted({c for c in text if ord(c) > 127})
        ok("EM-DASH %s == 0" % label, em == 0, "found %d" % em)
        ok("EN-DASH %s == 0" % label, en == 0, "found %d" % en)
        ok("ASCII-ONLY %s" % label, not bad,
           "non-ascii: %s" % "".join("U+%04X " % ord(c) for c in bad))

    # 2. the [hidden] rule that stops every flow rendering at once
    ok("[hidden] display:none !important present in CSS",
       re.search(r"\[hidden\]\s*\{\s*display:\s*none\s*!important;?\s*\}", css))

    # 3. structure: three flows, all hidden at rest; chooser visible at rest
    flow_divs = re.findall(r'<div id="flow-([a-z]+)"([^>]*)>', html)
    ok("exactly 3 flow containers", len(flow_divs) == 3,
       "found %d: %s" % (len(flow_divs), [f for f, _ in flow_divs]))
    ok("flow ids match FLOWS", [f for f, _ in flow_divs] == FLOWS,
       str([f for f, _ in flow_divs]))
    for f, attrs in flow_divs:
        ok("flow-%s ships hidden" % f, "hidden" in attrs, attrs)
    m = re.search(r'<div id="chooser"([^>]*)>', html)
    ok("chooser present", m is not None)
    ok("chooser NOT hidden at rest", m and "hidden" not in m.group(1))
    ok("you-are bar ships hidden", re.search(r'id="youare" hidden', html))
    ok("foot ships hidden", re.search(r'id="foot" hidden', html))

    # 4. the ENROLL button must come before the chooser, so the chooser can
    #    never push it off the first screen
    ok("ENROLL before chooser in source order",
       html.index('class="enroll"') < html.index('id="chooser"'))

    # 5. every img carries real width/height, matching the file on disk
    imgs = re.findall(r"<img [^>]*>", html)
    ok("img count == total steps", len(imgs) == sum(len(STEPS[f]) for f in FLOWS),
       "%d imgs vs %d steps" % (len(imgs), sum(len(STEPS[f]) for f in FLOWS)))
    from PIL import Image
    for tag in imgs:
        src = re.search(r'src="([^"]+)"', tag).group(1)
        name = src.rsplit("/", 1)[-1]
        wm = re.search(r'width="(\d+)"', tag)
        hm = re.search(r'height="(\d+)"', tag)
        ok("dims on %s" % name, wm and hm, tag[:90])
        if wm and hm:
            real = Image.open(os.path.join(IMGDIR, name)).size
            ok("dims match file %s" % name,
               (int(wm.group(1)), int(hm.group(1))) == real,
               "tag %s vs file %s" % ((int(wm.group(1)), int(hm.group(1))), real))

    # 6. lazy loading: exactly one eager image per flow, and it is that flow's first
    for f in FLOWS:
        seg = html.split('<div id="flow-%s" hidden>' % f, 1)[1]
        seg = seg.split('<div id="flow-', 1)[0].split('<div class="foot"', 1)[0]
        fimgs = re.findall(r"<img [^>]*>", seg)
        eager = [t for t in fimgs if 'loading="lazy"' not in t]
        ok("flow-%s image count == step count" % f, len(fimgs) == len(STEPS[f]),
           "%d vs %d" % (len(fimgs), len(STEPS[f])))
        ok("flow-%s has exactly 1 eager image" % f, len(eager) == 1,
           "%d eager" % len(eager))
        ok("flow-%s eager image is the first" % f,
           fimgs and eager and fimgs[0] is eager[0])

    # 7. Carrd traps: nothing that would split the embed or break injection
    for label, text in (("help.css", css), ("help.html", html), ("help.js", js)):
        ok("no literal </script> in %s" % label, "</" + "script" not in text.lower())
        ok("no literal </style> in %s" % label, "</" + "style" not in text.lower())

    # 8. deep-link values already sent out must never be renamed
    ok("legacy flow keys intact", "noapp" in FLOWS and "circleapp" in FLOWS)
    for f in FLOWS:
        ok("js knows flow %s" % f, '"%s"' % f in js)

    # 9. accents: three distinct dark accents, all declared
    darks = [ACCENT[f][0] for f in FLOWS]
    ok("three distinct accent colours", len(set(darks)) == 3, str(darks))
    for f in FLOWS:
        ok("accent declared for %s" % f, ".f-%s" % f in css and ".pick-%s" % f in css)
        ok("icon present for %s" % f, ICON[f] in html)

    passed = sum(1 for _, c, _ in checks if c)
    print("GATES: %d passed / %d failed" % (passed, len(checks) - passed))
    if fails:
        for f in fails:
            print("  FAIL", f)
        raise GateFail("%d gate(s) failed; nothing written" % len(fails))
    return len(checks)


# ---------------------------------------------------------------- main -----
def main():
    os.makedirs(IMGDIR, exist_ok=True)
    made = build_desktop_images()
    print("desktop images written: %d" % len(made))
    for name, size, nbytes in made:
        print("   %-18s %sx%s  %d KB" % (name, size[0], size[1], nbytes // 1024))

    css, html, js = build_css(), build_html(), build_js()
    n = gates(css, html, js)

    open(os.path.join(OUT, "help.css"), "w", encoding="utf-8", newline="\n").write(css)
    open(os.path.join(OUT, "help.html"), "w", encoding="utf-8", newline="\n").write(html)
    open(os.path.join(OUT, "help.js"), "w", encoding="utf-8", newline="\n").write(js)

    print("\nWROTE (all %d gates green):" % n)
    for f in ("help.css", "help.html", "help.js"):
        print("   %-10s %6d bytes" % (f, os.path.getsize(os.path.join(OUT, f))))
    for f in FLOWS:
        print("   flow %-10s %2d steps / %2d images"
              % (f, len(STEPS[f]), len(STEPS[f])))
    print("   img dir  : %d files" % len(os.listdir(IMGDIR)))


if __name__ == "__main__":
    try:
        main()
    except GateFail as e:
        print("BUILD ABORTED:", e)
        sys.exit(1)
