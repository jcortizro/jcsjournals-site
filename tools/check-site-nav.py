# THE CROSS-SITE MENU GATE. Fails (exit 1) unless every live page in the family carries the one shared menu:
#   jcj/          jcsjournals.com        current item: Free Course
#   td101page/    td101.carrd.co         current item: Free Course   (and byte-identical to jcj/)
#   library/      freelibrary.carrd.co   current item: Free Resource Library  (and no "Pick a topic" line)
#   recipebook/   freerecipes.carrd.co   current item: Free Recipe Book, in index.html (the live surface) and in the
#                                        three recipebook.* pieces
# For each page it parses the menu on its own (html.parser, not the regexes that wrote it) and requires exactly these
# three links and these four socials, in this order, written out below BY HAND rather than imported, so an edit to
# tools/site_nav.py that drops or reorders a link fails here instead of shipping. It then requires each copy to be
# exactly what tools/site_nav.py writes today (a stale copy fails), with its CSS and JS present once.
#
# Usage:  py -3.12 tools\check-site-nav.py               check the repo
#         py -3.12 tools\check-site-nav.py --root DIR    check a copy (how the gate is proven to fail)

import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

sys.dont_write_bytecode = True  # importing site_nav must not leave a __pycache__ folder in the repo
sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_nav

EXPECT_LINKS = [
    ("https://freelibrary.carrd.co/", "Free Resource Library"),
    ("https://freerecipes.carrd.co/", "Free Recipe Book"),
    ("https://jcsjournals.com/", "Free Course"),
]
EXPECT_SOCIALS = [
    ("https://www.facebook.com/jc.ortiz.roman/", "Facebook"),
    ("https://www.youtube.com/@jc_ortiz_roman", "YouTube"),
    ("https://www.instagram.com/jc.ortiz.roman/", "Instagram"),
    ("https://jcortizroman.substack.com/", "Substack"),
]
# (page, current url, site_nav key, css file or None when inline, js file or None when inline)
PAGES = [
    ("jcj/jcj.html", "https://jcsjournals.com/", "course", "jcj/jcj.css", "jcj/jcj.js"),
    ("td101page/jcj.html", "https://jcsjournals.com/", "course", "td101page/jcj.css", "td101page/jcj.js"),
    ("library/library.html", "https://freelibrary.carrd.co/", "library", "library/library.css", "library/library.js"),
    ("recipebook/index.html", "https://freerecipes.carrd.co/", "recipes", None, None),
    ("recipebook/recipebook.html", "https://freerecipes.carrd.co/", "recipes", "recipebook/recipebook.css",
     "recipebook/recipebook.js"),
]
START, END = "<!-- jcj-sitenav:start", "<!-- jcj-sitenav:end -->"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Menu(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.links, self.socials, self.cur = [], [], [], None
        self.ids, self.buttons = Counter(), []

    def _inside(self, key, val):
        return any(d.get(key) == val for _, d in self.stack)

    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        if "id" in a:
            self.ids[a["id"]] += 1
        if tag == "a" and self._inside("id", "jcj-menu"):
            rec = {"href": a.get("href"), "text": "", "target": a.get("target"), "rel": a.get("rel"),
                   "current": a.get("aria-current")}
            (self.socials if self._inside("id", "jcj-socials") else self.links).append(rec)
            self.cur = rec
        if tag == "button":
            self.buttons.append(a)
        if tag == "div" and a.get("id") == "jcj-socials":
            self.soc_hidden = "hidden" in a
        if tag not in VOID:
            self.stack.append((tag, a))

    def handle_endtag(self, tag):
        if tag == "a":
            self.cur = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return

    def handle_data(self, d):
        if self.cur is not None:
            self.cur["text"] += d


def check_page(root, page, cur_url, key, css_name, js_name, fails):
    p = root / page
    if not p.is_file():
        fails.append(f"{page}: missing")
        return
    html = p.read_text(encoding="utf-8")
    if html.count(START) != 1 or html.count(END) != 1:
        fails.append(f"{page}: menu block markers found {html.count(START)} start / {html.count(END)} end, want 1/1")
        return
    a = html.index(START)
    b = html.index(END) + len(END)
    block = html[a:b]
    m = Menu()
    m.feed(block)
    m.close()
    got_links = [(r["href"], " ".join(r["text"].split())) for r in m.links]
    if got_links != EXPECT_LINKS:
        fails.append(f"{page}: menu links {got_links} != expected {EXPECT_LINKS}")
    cur = [r["href"] for r in m.links if r["current"] == "page"]
    if cur != [cur_url]:
        fails.append(f"{page}: aria-current on {cur}, want exactly [{cur_url}]")
    for r in m.links:
        if r["target"] is not None:
            fails.append(f"{page}: site link {r['href']} has target={r['target']!r}; the free sites open in the same tab")
        if "#" in (r["href"] or ""):
            fails.append(f"{page}: site link {r['href']} carries a #hash (Carrd hijacks them)")
    got_soc = [(r["href"], " ".join(r["text"].split())) for r in m.socials]
    if got_soc != EXPECT_SOCIALS:
        fails.append(f"{page}: socials {got_soc} != expected {EXPECT_SOCIALS}")
    for r in m.socials:
        if r["target"] != "_blank" or r["rel"] != "noopener":
            fails.append(f"{page}: social {r['href']} must be target=_blank rel=noopener")
    if not getattr(m, "soc_hidden", False):
        fails.append(f"{page}: the socials list must start hidden")
    if not any(b.get("aria-controls") == "jcj-menu" for b in m.buttons):
        fails.append(f"{page}: no button opens the menu (aria-controls=jcj-menu)")
    if not any(b.get("aria-controls") == "jcj-socials" for b in m.buttons):
        fails.append(f"{page}: no Socials button (aria-controls=jcj-socials)")
    for idv in ("jcj-navbar", "jcj-menu", "jcj-socials", "jcj-navscrim"):
        n = html.count('id="%s"' % idv)
        if n != 1:
            fails.append('%s: id="%s" appears %d times, want 1' % (page, idv, n))
    if '<header class="site-header"' in html or 'class="topbar' in html:
        fails.append(f"{page}: an old site header is still on the page")
    # stale copy check: exactly what tools/site_nav.py writes today
    want = site_nav.inline_block(key) if css_name is None else site_nav.html_block(key)
    if block != want:
        fails.append(f"{page}: menu block differs from tools/site_nav.py (stale copy; re-run the build)")
    if css_name is not None:
        css = (root / css_name).read_text(encoding="utf-8")
        js = (root / js_name).read_text(encoding="utf-8")
        if css.count(site_nav.css_block()) != 1:
            fails.append(f"{css_name}: the menu CSS block appears {css.count(site_nav.css_block())} times, want 1")
        if js.count(site_nav.js_block()) != 1:
            fails.append(f"{js_name}: the menu JS block appears {js.count(site_nav.js_block())} times, want 1")


def main():
    root = Path(__file__).resolve().parent.parent
    if "--root" in sys.argv:
        root = Path(sys.argv[sys.argv.index("--root") + 1]).resolve()
    fails = []
    for page, cur_url, key, css_name, js_name in PAGES:
        before = len(fails)
        check_page(root, page, cur_url, key, css_name, js_name, fails)
        print(("  ok    " if len(fails) == before else "  FAIL  ") + page)
    # the library: JC deleted "Pick a topic below; each one opens right where it is." (26 Oct 2026)
    for fn in ("library/library.html", "library/library.css", "library/library.js"):
        p = root / fn
        if p.is_file() and "pick a topic" in p.read_text(encoding="utf-8").lower():
            fails.append(f"{fn}: contains 'Pick a topic' (JC deleted that line)")
    # the course page is one page served twice: jcj/ (jcsjournals.com) must be a byte copy of td101page/
    for fn in ("jcj.html", "jcj.css", "jcj.js"):
        x, y = root / "jcj" / fn, root / "td101page" / fn
        if not (x.is_file() and y.is_file() and x.read_bytes() == y.read_bytes()):
            fails.append(f"jcj/{fn} is not byte-identical to td101page/{fn}")
    if fails:
        print(f"check-site-nav: FAIL, {len(fails)} problem(s):")
        for f in fails:
            print("  - " + f)
        sys.exit(1)
    print(f"check-site-nav: PASS ({len(PAGES)} pages, 3 links + 4 socials each, in order; no 'Pick a topic'; jcj == td101page)")


if __name__ == "__main__":
    main()
