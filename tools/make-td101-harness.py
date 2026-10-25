# Make the local test harness for the TD101 page: the REAL jcsjournals.com Carrd shell (saved
# 2026-10-25), with only its loader's base URL pointed at the local td101page/ folder and its own
# relative assets pointed back at jcsjournals.com. So the test runs inside Carrd's real CSS and
# JavaScript (including its hash hijacking), with the new page loaded exactly the way it will be live.
#
# Serve the repo root:   py -3.12 -m http.server 8765 --bind 127.0.0.1
# Desktop:               http://127.0.0.1:8765/tools/carrd-test-td101.html
# Phone width (390px):   http://127.0.0.1:8765/tools/mobile-test-td101.html

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
shell = (ROOT / "src" / "td101-page" / "carrd-shell-live-2026-10-25.html").read_text(encoding="utf-8")

LIVE_BASE = 'var base="https://raw.githubusercontent.com/jcortizro/jcsjournals-site/main/jcj/"'
TEST_BASE = 'var base="/td101page/"'
if shell.count(LIVE_BASE) != 1:
    raise SystemExit(f"REFUSED: expected the live loader base exactly once, found {shell.count(LIVE_BASE)}")
out = shell.replace(LIVE_BASE, TEST_BASE)
out = out.replace('"assets/', '"https://jcsjournals.com/assets/').replace("'assets/", "'https://jcsjournals.com/assets/")
out = out.replace("(assets/", "(https://jcsjournals.com/assets/")
if LIVE_BASE in out or TEST_BASE not in out:
    raise SystemExit("REFUSED: loader base not switched")
if '"assets/' in out:
    raise SystemExit("REFUSED: a relative asset path survived")
(ROOT / "tools" / "carrd-test-td101.html").write_text(out, encoding="utf-8", newline="\n")

# Tracking probe: the same page plus a recorder that writes, at four moments after load, the address's
# query string, the kuid Kartra's form is holding, and the country-code dropdown's widths. Open it as
#   /tools/carrd-test-td101-track.html?kuid=<uuid>-<unix ts>&kref=<url>&lid=<id>
# and the recorder line should show the kuid param adopted into the form, then stripped from the address.
TRACK = """
<div id="trk"></div>
<script>
(function(){var t0=Date.now();function rec(){var d=document.getElementById('trk');var k=document.querySelector('#jcj-page input[name="kuid"]');var cc=document.querySelector('#jcj-page .for_country_code');var ccb=cc&&cc.querySelector('.kartra_optin_dropdown-toggle');var pw=cc&&cc.parentElement;d.textContent+=' || t='+(Date.now()-t0)+' search='+JSON.stringify(location.search)+' kuidField='+(k?k.value:'none')+' kuuid='+(window.kuuid||'')+' kref='+(window.kref||'')+' ccW='+(cc?Math.round(cc.getBoundingClientRect().width):'-')+' pwW='+(pw?Math.round(pw.getBoundingClientRect().width):'-')+' btnW='+(ccb?Math.round(ccb.getBoundingClientRect().width):'-')+' forms='+document.querySelectorAll('#jcj-page form').length;}
[800,2500,6000,10000].forEach(function(ms){setTimeout(rec,ms)});})();
</script>
</body>"""
if out.count("</body>") != 1:
    raise SystemExit("REFUSED: expected one </body> in the shell")
(ROOT / "tools" / "carrd-test-td101-track.html").write_text(out.replace("</body>", TRACK), encoding="utf-8", newline="\n")

mobile = """<!doctype html>
<html>
<head><meta charset="utf-8"><title>td101 mobile test</title>
<style>
  body{margin:0;background:#222;display:flex;flex-direction:column;align-items:center;gap:10px;padding:14px;font-family:sans-serif}
  iframe{width:390px;height:844px;border:2px solid #555;background:#000}
</style>
</head>
<body>
<!-- Phone-width harness: the real Carrd shell replica at a true 390px. -->
<iframe id="f" src="carrd-test-td101.html"></iframe>
<script>/* ?h=9000 makes the phone frame tall enough for a full-page screenshot */
var h=new URLSearchParams(location.search).get('h');if(h)document.getElementById('f').style.height=h+'px';</script>
</body>
</html>
"""
(ROOT / "tools" / "mobile-test-td101.html").write_text(mobile, encoding="utf-8", newline="\n")
print("harness written: tools/carrd-test-td101.html, tools/mobile-test-td101.html")
