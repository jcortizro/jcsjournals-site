# Writes jcj/ (jcsjournals.com) from td101page/ (td101.carrd.co), plus the webinar banner when it is switched on.
#
# THE ONE SWITCH is BANNER_ON below.
#   True  : jcj/jcj.html = td101page/jcj.html with src/jcj-banner/webinar-banner.html inserted at the very top,
#           right above the shared menu bar. jcj.css and jcj.js stay byte copies.
#   False : jcj/ = byte copy of td101page/ (exactly what build-all.ps1 did before 18 Nov 2026).
# td101page/ is never touched here, so td101.carrd.co never shows the banner.
#
# Optional picture: if src/jcj-banner/landscape.webp (or .jpg) exists, it is embedded as a data URI above the
# line and links to the same sign-up URL. If not, the banner is the line and the button only.
#
# Usage:  py -3.12 tools\jcj-banner.py      (build-all.ps1 runs it after build-td101-page.py)
# Then:   py -3.12 tools\check-site-nav.py  must PASS before any push.

import base64, sys
from pathlib import Path

BANNER_ON = True  # Fri 20 Nov 2026: set to False, run this script, run check-site-nav.py, commit, push.

ROOT = Path(__file__).resolve().parent.parent
SRC, DST = ROOT / "td101page", ROOT / "jcj"
PART = ROOT / "src" / "jcj-banner" / "webinar-banner.html"
IMGS = [ROOT / "src" / "jcj-banner" / "landscape.webp", ROOT / "src" / "jcj-banner" / "landscape.jpg"]
NAV = "<!-- jcj-sitenav:start"
B_START, B_END = "<!-- jcj-webinar-banner:start", "<!-- jcj-webinar-banner:end -->"
URL = "https://go.mucusfreelife.com/webinar-jc-site"


def fail(msg):
    print("jcj-banner: REFUSED, " + msg)
    sys.exit(1)


def banner_block():
    part = PART.read_text(encoding="utf-8")
    img = next((p for p in IMGS if p.is_file()), None)
    tag = ""
    if img:
        mime = "image/webp" if img.suffix == ".webp" else "image/jpeg"
        data = base64.b64encode(img.read_bytes()).decode("ascii")
        tag = (f'<a class="jw-img" href="{URL}" target="_blank" rel="noopener">'
               f'<img src="data:{mime};base64,{data}" width="1200" height="630" alt="Free live class, Thu Nov 19"></a>')
    if part.count("{{IMAGE}}") != 1:
        fail("part file must hold {{IMAGE}} exactly once")
    block = part.replace("{{IMAGE}}", tag).rstrip("\n") + "\n"
    for s, n in ((B_START, 1), (B_END, 1), (f'href="{URL}"', 2 if img else 1), ('target="_blank"', 2 if img else 1)):
        if block.count(s) != n:
            fail(f"banner block holds {s!r} {block.count(s)} times, want {n}")
    if chr(0x2014) in block or chr(0x2013) in block:
        fail("banner block holds a dash character that is banned")
    return block, bool(img)


def main():
    for fn in ("jcj.css", "jcj.js"):
        (DST / fn).write_bytes((SRC / fn).read_bytes())
    html = (SRC / "jcj.html").read_bytes().decode("utf-8")
    if B_START in html:
        fail("td101page/jcj.html already carries the banner; it must never")
    if not BANNER_ON:
        (DST / "jcj.html").write_bytes(html.encode("utf-8"))
        print("jcj-banner: OFF, jcj/ is a byte copy of td101page/")
        return
    if html.count(NAV) != 1:
        fail(f"menu start marker found {html.count(NAV)} times, want 1")
    block, has_img = banner_block()
    out = html.replace(NAV, block + NAV, 1)
    if out.count(B_START) != 1 or out.index(B_START) > out.index(NAV):
        fail("banner not placed exactly once above the menu")
    if out.replace(block, "", 1) != html:
        fail("output minus the banner is not td101page/jcj.html")
    (DST / "jcj.html").write_bytes(out.encode("utf-8"))
    print(f"jcj-banner: ON ({'with' if has_img else 'without'} picture), banner {len(block):,} chars above the menu")


if __name__ == "__main__":
    main()
