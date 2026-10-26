# jcsjournals-site

Code for JC's live websites. Each Carrd site holds one small Embed(Code)
snippet that loads the real page from **raw.githubusercontent.com** (not jsDelivr,
its cache served stale files). Push here and the live pages update in ~5 minutes.
JC never re-pastes the snippets.

## Which site loads what (measured 2026-10-26)

| Live site | Loads from this repo | Built by | Snippet in Carrd |
|---|---|---|---|
| https://jcsjournals.com | `jcj\` (a byte copy of `td101page\`) | `tools\build-td101-page.py`, then copied by `tools\build-all.ps1` | `carrd-embed-jcj.html` |
| https://td101.carrd.co | `td101page\` (the same TD101 course page) | `tools\build-td101-page.py` | `carrd-embed-td101test.html` |
| https://freelibrary.carrd.co | `library\` | `tools\build-library-page.ps1` + `tools\split-library.ps1` | `carrd-embed-library.html` |
| https://freerecipes.carrd.co | `recipebook\index.html` | `export_to_site.py` on JC's other machine, then `tools\add-site-nav.py recipebook` | its own loader, see "The recipe book page" |
| https://circlehelp.carrd.co | `td101help\` | `tools\td101help-build\` | `carrd-embed-td101help.html` |

`home\` (the old landing page, `carrd-embed-home.html`) and `signup\` (the old
td101.carrd.co waitlist, `carrd-embed-signup.html`) are not loaded by any site
in this table.

## The site menu (one copy for every site)

The bar at the top of jcsjournals.com, td101.carrd.co, freelibrary and
freerecipes ("JC's Journals | FREE RESOURCES ->" and the three lines) is written
ONCE, in `tools\site_nav.py`: the links (Free Resource Library, Free Recipe Book,
Free Course), the four socials, its CSS and its script. The course build imports
it, `tools\add-site-nav.py` puts it into the library and the recipe book, and
`tools\check-site-nav.py` fails the build if any page is missing it, carries an
old copy, or has the links out of order. So to change a link or a word, edit
`tools\site_nav.py` and run `tools\build-all.ps1`; never edit the copies in the
pages, the next build overwrites them.

## Build

    tools\build-all.ps1      # then: git add -A; git commit; git push

It rebuilds home, the library (with the menu), the course page (td101page\,
copied over jcj\), re-applies the menu to the recipe book, and ends with
`tools\check-site-nav.py`. If that last check fails, do not push.

⛔ Never run `build-jcj-page.ps1`, `split-jcj.ps1`, `build-signup-page.ps1` or
`split-signup.ps1`. The first two rebuilt jcj\ from the OLD hub and would replace
the live jcsjournals.com course page (`split-jcj.ps1` now refuses to run); the
other two rebuild the old waitlist that no live site shows. `build-all.ps1` no
longer calls any of them.

## Edit these (sources)

- `tools\site_nav.py`: the site menu on all four sites (see above).
- `src\td101-page\`: the TD101 course page (JC's cut + Spira's Kartra form),
  built by `tools\build-td101-page.py` into td101page\ (and so jcj\).
- `src\home.part.html`: the landing page AND the shared shell (background,
  dropdown, buttons) the library page is generated from.
- `site-masters\mdhs-v4-final.html` (on D:), the library's copy master: JC's
  locked article text + library component CSS/JS.
- `src\shared\dock.*`: the floating Resources/Socials dock at the bottom of the
  library.
- `tools\urls.ps1`: the page URLs the library build uses. **Changing a domain =
  edit here (and in tools\site_nav.py), build, push.**
- `src\`: foliage.jpg + the embedded font CSS.
- `src\jcj-parts\`: blocks of the OLD hub (retired 2026-10-26, see Build).

## The recipe book page

`recipebook\*` is generated from a DIFFERENT project: `C:\ClaudeWork\Recipe Book\`
on JC's other machine. That folder holds the book's own generator (one template
plus one data table). To update the live recipe book:

    cd C:\ClaudeWork\Recipe Book
    python build_book.py        # redraw all 50 pages from recipes_data.json
    python export_to_site.py    # split into this repo's recipebook\ folder
    cd C:\Users\taino\jcsjournals-site
    py -3.12 tools\add-site-nav.py recipebook   # ⛔ EVERY TIME, see below
    py -3.12 tools\check-site-nav.py
    git add -A; git commit -m "..."; git push

⛔ **After every export, run `py -3.12 tools\add-site-nav.py recipebook` before
committing.** The export overwrites recipebook\ completely, so it wipes the site
menu and brings back the old wordmark header. The injector puts the menu back
(it replaces the old header, or an older copy of the menu) and is safe to run any
number of times. `tools\check-site-nav.py` fails if it was skipped.

The export writes four files, two surfaces from one source:

- `index.html`, the whole book as one document. **This is what
  freerecipes.carrd.co shows.** Its Carrd loader first asks for
  `jcortizro/td101-recipe-book/main/index.html` (a 404 on 2026-10-26) and then
  falls back to this repo's `recipebook\index.html`, parses it, puts every
  `<style>` in the page head and runs every `<script>`. If that other repo ever
  starts answering, the live page switches to it, and the menu has to be applied
  there too.
- `recipebook.css` / `.html` / `.js`, the three-piece surface that
  `carrd-embed-recipebook.html` fetches (no live site uses it today). It carries
  the menu too.

Apart from the menu, do not hand-edit any of them here; they are overwritten on
every export.

Local test harnesses: `tools\embed-test-recipebook.html` (the live loader,
`?pieces=1` for the three pieces) and `tools\mobile-test-recipebook.html`
(320 / 360 / 390 px).

## Hosting the recipe book on GitHub Pages

This repo is public, so Pages can also serve the book (and its PDF) with no
Carrd site. Two one-time steps, both JC's:

    cd C:\Users\taino\jcsjournals-site
    git push origin main

Then github.com/jcortizro/jcsjournals-site, Settings, Pages, "Deploy from a
branch", Branch: main, folder: / (root), Save. The book is then at

    https://jcortizro.github.io/jcsjournals-site/recipebook/

## Never hand-edit (generated)

`jcj\*`, `td101page\*`, `home\*`, `library\*`, the menu block in
`recipebook\*`, `site-masters\mfl-home-redesign-v1.html`,
`site-masters\mdhs-library-page.html`.

## Notes

- Background must stay as `.bg-photo` / `.bg-scrim` fixed divs. Carrd overrides
  `body::before/after`, which made the dark background fade out after ~2s.
- `tools\build-combined.ps1` is parked (one-page merge experiment, rejected).
- Full context: `JC Website\files\20-HANDOFF-2026-07-19-LIVE-SITE.md`.
