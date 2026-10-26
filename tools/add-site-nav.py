# Put the one shared site menu (tools/site_nav.py) into the pages that are NOT built by a Python builder:
#   library     -> library/library.html (+ .css, .js)            freelibrary.carrd.co, current item: Free Resource Library
#   recipebook  -> recipebook/index.html (menu + its own style and script inline)
#                  recipebook/recipebook.html (+ .css, .js)       current item: Free Recipe Book
# (jcsjournals.com and td101.carrd.co get the same menu from tools/build-td101-page.py.)
#
# WHY AN INJECTOR: the recipe book is generated on JC's other machine (C:\ClaudeWork\Recipe Book\export_to_site.py)
# and every export overwrites recipebook/ completely, menu included. So after EVERY recipe book export, run
#     py -3.12 tools\add-site-nav.py recipebook
# before committing. The library build (split-library.ps1) runs it for the library by itself.
#
# MEASURED 2026-10-26: freerecipes.carrd.co serves recipebook/index.html, not the three recipebook.* pieces. Its Carrd
# loader first asks for raw jcortizro/td101-recipe-book/main/index.html (404 today), then falls back to this repo's
# recipebook/index.html, parses it with DOMParser, puts every <style> in the head and runs every <script> after
# mounting. That is why index.html carries the menu with its own <style> and <script> beside the markup.
#
# SAFE TO RE-RUN ANY NUMBER OF TIMES. Where the menu goes, in order:
#   1. an existing menu block (between the jcj-sitenav start/end comments) is replaced with the current one;
#   2. else the slot comment the library build leaves (<!-- jcj-sitenav-slot -->);
#   3. else the old site header (<header class="site-header">...</header>, wordmark + icons) is replaced;
#   4. else the menu goes at the very top (recipebook.html: above the book's own header block, which stays).
#   CSS is appended to the .css file, JS is put FIRST in the .js file (so an error later in the page's own script
#   cannot stop the menu). Same markers, so a re-run replaces instead of adding a second copy.
# Every result is checked in memory BEFORE the file is opened for writing: one menu, no old header, no slot left,
# no control bytes, no new U+FFFD. A file that would not change is not rewritten.
#
# Usage:  py -3.12 tools\add-site-nav.py library | recipebook | all

import re, sys
from pathlib import Path

sys.dont_write_bytecode = True  # importing site_nav must not leave a __pycache__ folder in the repo
import site_nav

ROOT = Path(__file__).resolve().parent.parent
HTML_BLOCK_RX = re.compile(r"<!-- jcj-sitenav:start.*?<!-- jcj-sitenav:end -->", re.S)
CODE_BLOCK_RX = re.compile(r"/\* jcj-sitenav:start.*?/\* jcj-sitenav:end \*/", re.S)
SLOT = "<!-- jcj-sitenav-slot -->"
OLD_HEADER_RX = re.compile(r'<header class="site-header">.*?</header>', re.S)
BODY_RX = re.compile(r"<body[^>]*>")


def refuse(msg):
    raise SystemExit("REFUSED: " + msg)


def bad_bytes(s):
    return [(i, hex(ord(c))) for i, c in enumerate(s)
            if (ord(c) < 0x20 and c not in "\t\n\r") or 0x7F <= ord(c) <= 0x9F]


def place_html(text, block, where, name):
    n = len(HTML_BLOCK_RX.findall(text))
    starts, ends = text.count("<!-- jcj-sitenav:start"), text.count("<!-- jcj-sitenav:end -->")
    if n > 1 or starts != n or ends != n:
        refuse(f"{name}: found {n} menu block(s), {starts} start and {ends} end markers; fix by hand, nothing written")
    if n == 1:
        return HTML_BLOCK_RX.sub(lambda m: block, text), "menu replaced"
    if text.count(SLOT) == 1:
        return text.replace(SLOT, block), "slot filled"
    hdr = OLD_HEADER_RX.findall(text)
    if len(hdr) == 1:
        return OLD_HEADER_RX.sub(lambda m: block, text), "old site header replaced"
    if len(hdr) > 1:
        refuse(f"{name}: {len(hdr)} old site headers, expected at most 1")
    if where == "top":
        return block + "\n" + text, "added at the top"
    if where == "body":
        b = BODY_RX.findall(text)
        if len(b) != 1:
            refuse(f"{name}: expected one <body> tag, found {len(b)}")
        return BODY_RX.sub(lambda m: m.group(0) + "\n" + block, text, count=1), "added after <body>"
    refuse(f"{name}: no place for the menu")


def place_code(text, block, at_start, name):
    n = len(CODE_BLOCK_RX.findall(text))
    if n > 1 or text.count("/* jcj-sitenav:start") != n or text.count("/* jcj-sitenav:end */") != n:
        refuse(f"{name}: found {n} menu code block(s) with unbalanced markers; fix by hand, nothing written")
    if n == 1:
        return CODE_BLOCK_RX.sub(lambda m: block, text), "replaced"
    if at_start:
        return block + "\n" + text, "added first"
    return text.rstrip("\n") + "\n" + block + "\n", "appended"


def check_page(new, old, name, current):
    problems = []
    if len(HTML_BLOCK_RX.findall(new)) != 1:
        problems.append("menu block count is not 1")
    if site_nav.nav_html(current) not in new:
        problems.append("the current menu markup is not in the result")
    if OLD_HEADER_RX.search(new):
        problems.append("the old site header is still there")
    if SLOT in new:
        problems.append("the slot comment is still there")
    if new.count('id="jcj-navbar"') != 1:
        problems.append('id="jcj-navbar" count is not 1')
    return problems


def finish(path, old, new, problems, how, results):
    name = path.relative_to(ROOT).as_posix()
    cb = bad_bytes(new)
    if cb:
        problems.append(f"{len(cb)} control byte(s), first at {cb[:3]}")
    if new.count("\ufffd") > old.count("\ufffd"):
        problems.append("U+FFFD added")
    if "\u2014" in new and "\u2014" not in old:
        problems.append("em dash added")
    if problems:
        refuse(f"{name}: " + "; ".join(problems) + " (nothing written)")
    results.append((path, old, new, f"{name}: {how}" + (" (no change)" if new == old else "")))


def read(path):
    if not path.is_file():
        refuse(f"missing {path}")
    return path.read_text(encoding="utf-8")  # universal newlines: a CRLF checkout reads as LF


def do_library(results):
    d = ROOT / "library"
    p = d / "library.html"
    old = read(p)
    new, how = place_html(old, site_nav.html_block("library"), "top", "library.html")
    probs = check_page(new, old, "library.html", "library")
    if "Pick a topic" in new:
        probs.append("'Pick a topic below' is back (JC deleted it 2026-10-26)")
    finish(p, old, new, probs, how, results)
    for fn, at_start, block in (("library.css", False, site_nav.css_block()), ("library.js", True, site_nav.js_block())):
        p = d / fn
        old = read(p)
        new, how = place_code(old, block, at_start, fn)
        finish(p, old, new, [] if new.count(block) == 1 else ["menu code count is not 1"], how, results)


def do_recipebook(results):
    d = ROOT / "recipebook"
    # the live surface: one file, menu with its own <style> and <script>
    p = d / "index.html"
    old = read(p)
    new, how = place_html(old, site_nav.inline_block("recipes"), "body", "index.html")
    probs = check_page(new, old, "index.html", "recipes")
    if new.count(site_nav.inline_block("recipes")) != 1:
        probs.append("inline menu (markup + style + script) count is not 1")
    finish(p, old, new, probs, how, results)
    # the three-piece surface (carrd-embed-recipebook.html), kept in step so either surface carries the menu
    p = d / "recipebook.html"
    old = read(p)
    new, how = place_html(old, site_nav.html_block("recipes"), "top", "recipebook.html")
    finish(p, old, new, check_page(new, old, "recipebook.html", "recipes"), how, results)
    for fn, at_start, block in (("recipebook.css", False, site_nav.css_block()), ("recipebook.js", True, site_nav.js_block())):
        p = d / fn
        old = read(p)
        new, how = place_code(old, block, at_start, fn)
        finish(p, old, new, [] if new.count(block) == 1 else ["menu code count is not 1"], how, results)


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg not in ("library", "recipebook", "all"):
        raise SystemExit("usage: py -3.12 tools\\add-site-nav.py library | recipebook | all")
    results = []
    if arg in ("library", "all"):
        do_library(results)
    if arg in ("recipebook", "all"):
        do_recipebook(results)
    # every file passed its checks in memory; only now is anything written, and only what changes
    for path, old, new, msg in results:
        if new != old:
            path.write_text(new, encoding="utf-8", newline="\n")
            if path.read_text(encoding="utf-8") != new:
                refuse(f"{path.name}: readback differs from what was written")
        print("  " + msg)
    print("add-site-nav OK")


if __name__ == "__main__":
    main()
