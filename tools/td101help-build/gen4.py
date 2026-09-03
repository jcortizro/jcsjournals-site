# -*- coding: utf-8 -*-
# Builds the td101help page into the jcsjournals-site repo working tree:
#   td101help/help.css, help.html, help.js, img/*.webp  + carrd-embed-td101help.html
import os, shutil, importlib.util

SCRATCH = os.path.dirname(os.path.abspath(__file__))
REPO = r"C:\Users\taino\jcsjournals-site"
OUT = os.path.join(REPO, "td101help")
RAW = "https://raw.githubusercontent.com/jcortizro/jcsjournals-site/main/td101help/"

spec = importlib.util.spec_from_file_location("g3", os.path.join(SCRATCH, "gen3.py"))
# gen3 rebuilds deploy/ pages on import; that is idempotent and stays in scratch.
g3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g3)

os.makedirs(os.path.join(OUT, "img"), exist_ok=True)

# images: flat dir, variant-prefixed
for var, src, n in (("noapp", "deploy/noapp/img", 15), ("circleapp", "deploy/circleapp/img", 16)):
    for i in range(1, n + 1):
        shutil.copyfile(os.path.join(SCRATCH, src, "%02d.webp" % i),
                        os.path.join(OUT, "img", "%s-%02d.webp" % (var, i)))

CSS = g3.CSS + """
  /* [hidden] must beat any author display rule (waitlist lesson, 2026-08-11) */
  [hidden] { display: none !important; }
  .chooser { display:flex; gap:10px; margin-top:16px; }
  .chooser button { flex:1; border:2px solid var(--green); background:#fff; color:var(--green);
      font:800 15px -apple-system,"Segoe UI",Roboto,Arial,sans-serif; border-radius:12px;
      padding:12px 8px; cursor:pointer; }
  .chooser button[aria-pressed="true"] { background:var(--green); color:#fff; }
  .chooser button:focus-visible { outline:3px solid var(--gold); outline-offset:2px; }
  body { background: var(--cream); }
"""

def steps_html(steps, var):
    from PIL import Image
    parts = []
    for i, (title, bullets, onlyif) in enumerate(steps, 1):
        im = Image.open(os.path.join(OUT, "img", "%s-%02d.webp" % (var, i)))
        w, h = im.size
        cls = "step onlyif" if onlyif else "step"
        head = ('<div><span class="chip">ONLY IF</span><h2>%s</h2></div>' % title) if onlyif else ('<h2>%s</h2>' % title)
        lis = "".join("<li>%s</li>" % b for b in bullets)
        lazy = '' if i == 1 else ' loading="lazy"'
        parts.append('<section class="%s"><header><div class="num">%d</div>%s</header>'
                     '<ul>%s</ul><img src="%simg/%s-%02d.webp" width="%d" height="%d" '
                     'alt="Step %d screenshot" decoding="async"%s></section>'
                     % (cls, i, head, lis, RAW, var, i, w, h, i, lazy))
    return "\n".join(parts)

def hero(sub):
    return ('<div class="hero"><p class="eyebrow">Transition Diet 101</p>'
            '<h1>%s</h1><p class="herosub">%s</p>'
            '<a class="enroll" href="%s">%s<span>%s</span></a>'
            '<div class="chooser" role="tablist">'
            '<button id="btn-noapp" aria-pressed="true">No app needed</button>'
            '<button id="btn-circleapp" aria-pressed="false">With the Circle app</button>'
            '</div></div>'
            % (g3.TITLE, sub, g3.ENROLL_HREF, g3.ENROLL_TEXT, g3.ENROLL_SUB))

foot = ('<div class="foot"><h3>%s</h3><p>%s</p>'
        '<a class="helpbtn" href="%s">Get help here</a>'
        '<p class="small">%s</p></div>' % (g3.FOOT_1, g3.FOOT_2, g3.HELP_HREF, g3.FOOT_3))
stick = '<div class="stick"><span>%s</span><a href="%s">Get help</a></div>' % (g3.FOOT_1, g3.HELP_HREF)

html = ('<div class="wrap">'
        + hero(g3.NOAPP_SUB)
        + '<div id="flow-noapp">' + steps_html(g3.NOAPP_STEPS, "noapp") + '</div>'
        + '<div id="flow-circleapp" hidden>' + steps_html(g3.APP_STEPS, "circleapp") + '</div>'
        + foot + '</div>' + stick)

JS = """
(function(){
  var subs = {
    noapp: %r,
    circleapp: %r
  };
  function show(which){
    var other = which === "noapp" ? "circleapp" : "noapp";
    document.getElementById("flow-" + which).hidden = false;
    document.getElementById("flow-" + other).hidden = true;
    document.getElementById("btn-" + which).setAttribute("aria-pressed", "true");
    document.getElementById("btn-" + other).setAttribute("aria-pressed", "false");
    var s = document.querySelector(".herosub");
    if (s) s.textContent = subs[which];
    if (location.hash !== "#" + which) history.replaceState(null, "", "#" + which);
    window.scrollTo(0, 0);
  }
  document.getElementById("btn-noapp").addEventListener("click", function(){ show("noapp"); });
  document.getElementById("btn-circleapp").addEventListener("click", function(){ show("circleapp"); });
  if (location.hash === "#circleapp") show("circleapp");
})();
""" % (g3.NOAPP_SUB, g3.APP_SUB)

open(os.path.join(OUT, "help.css"), "w", encoding="utf-8").write(CSS)
open(os.path.join(OUT, "help.html"), "w", encoding="utf-8").write(html)
open(os.path.join(OUT, "help.js"), "w", encoding="utf-8").write(JS)

LOADER = """<!-- TD 101 HOW-TO-GET-IN PAGE - Carrd Embed loader (test site for now).
     Paste this whole block into a Carrd "Embed" element, Type: Code, then
     Publish. After that you never touch Carrd again: rebuild, push, and the
     live page updates itself.
     Same two Carrd traps as the other loaders: code is flattened to one line
     (block comments only) and Carrd splits at a literal closing script tag
     (fragments carry no script tags; help.js is injected as text). -->
<script>
(function(){
  var base="%s";
  function hide(){
    Array.prototype.forEach.call(document.body.children,function(c){
      if(c.tagName!=="SCRIPT"&&c.tagName!=="STYLE"&&c.tagName!=="LINK")c.style.display="none";
    });
  }
  var opt={cache:'no-cache'};
  Promise.all([
    fetch(base+"help.css",opt).then(function(r){return r.text()}),
    fetch(base+"help.html",opt).then(function(r){return r.text()}),
    fetch(base+"help.js",opt).then(function(r){return r.text()})
  ]).then(function(a){
    var st=document.createElement("style");st.textContent=a[0];document.head.appendChild(st);
    hide();
    var d=document.createElement("div");d.id="td101help-page";d.innerHTML=a[1];
    document.body.appendChild(d);
    var s=document.createElement("script");s.textContent=a[2];document.body.appendChild(s);
  }).catch(function(){
    hide();
    var d=document.createElement("div");
    d.style.cssText="font:16px/1.6 system-ui,sans-serif;color:#E4BE3F;background:#0a0f0a;padding:48px 24px;text-align:center;min-height:100vh";
    d.innerHTML="<b>The walkthrough page is not published yet.</b><br>Push the repo and this page fills itself in, no re-paste needed.";
    document.body.appendChild(d);
  });
})();
</script>
""" % RAW
open(os.path.join(REPO, "carrd-embed-td101help.html"), "w", encoding="utf-8").write(LOADER)

for f in ("help.css", "help.html", "help.js"):
    print(f, os.path.getsize(os.path.join(OUT, f)) // 1024, "KB")
n = len(os.listdir(os.path.join(OUT, "img")))
print("img files:", n)
h = open(os.path.join(OUT, "help.html"), encoding="utf-8").read()
print("em-dashes:", h.count(chr(8212)), "| steps total:", h.count('class="step'))
