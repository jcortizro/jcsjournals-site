# jcsjournals-site

Code for JC's live website. Two Carrd pages, each holding one small Embed(Code)
snippet that loads the real page from **raw.githubusercontent.com** (not jsDelivr,
its cache served stale files). Push here and the live pages update in ~5 minutes.
JC never re-pastes the snippets.

| Page | Live | Snippet |
|---|---|---|
| Landing (Free/Paid) | https://td101landing.carrd.co/ | `carrd-embed-home.html` |
| Library | https://td101library.carrd.co/ | `carrd-embed-library.html` |
| JC's Journals | https://jcsjournals.com (JC attaches in Carrd) | `carrd-embed-jcj.html` |
| TD 101 Recipe Book | GitHub Pages, see below. No Carrd page yet | `recipebook\index.html`, or `carrd-embed-recipebook.html` for a Carrd surface |

## Hosting the recipe book on GitHub Pages

The book is the one page here that does not need a Carrd site. This repo is
already public, so Pages costs nothing extra, uses none of the ten Carrd
sites, serves the PDF from the same place, and its Contents links work
without the delegated-scroll fix Carrd's hash hijacking would force.

Two one-time steps, both JC's:

    cd C:\Users\taino\jcsjournals-site
    git push origin main

Then github.com/jcortizro/jcsjournals-site, Settings, Pages, "Deploy from a
branch", Branch: main, folder: / (root), Save. The book is then at

    https://jcortizro.github.io/jcsjournals-site/recipebook/

This does not rule out the Carrd surface. Both read the same folder, so
pasting `carrd-embed-recipebook.html` into an Embed(Code) element on a Carrd
page still works later with no rework.

## Build

    tools\build-all.ps1      # then: git add -A; git commit; git push

## Edit these (sources)

- `src\home.part.html`: the landing page AND the shared shell (background,
  header, dropdown, buttons). The library page is generated from this file, so
  shell edits hit both pages.
- `src\jcj-parts\`: the JC's Journals page's rebrand blocks (header, socials,
  footer, full legal docs, extra CSS). The jcj page is generated FROM the
  library master by `tools\build-jcj-page.ps1`, so library copy edits flow into
  it automatically; free/paid stay parked as "coming soon" there.
- `site-masters\mdhs-v4-final.html` (on D:), the library's copy master: JC's
  locked article text + library component CSS/JS.
- `tools\urls.ps1`: the two page URLs. **Changing a domain = edit here, build, push.**
- `src\`: foliage.jpg + the embedded font CSS.

## The recipe book page

`recipebook\*` is generated from a DIFFERENT project: `C:\ClaudeWork\Recipe Book\`.
That folder holds the book's own generator (one template plus one data table).
To update the live recipe book:

    cd C:\ClaudeWork\Recipe Book
    python build_book.py        # redraw all 50 pages from recipes_data.json
    python export_to_site.py    # split into this repo's recipebook\ folder
    cd C:\Users\taino\jcsjournals-site
    git add -A; git commit -m "..."; git push

The export writes four files, two surfaces from one source:

- `index.html`, the whole book as one document. This is the Pages url, the
  one a person can just open.
- `recipebook.css` / `.html` / `.js`, the three pieces the Carrd loader
  fetches separately.

Do not hand-edit any of them here, they are overwritten on every export.

## Never hand-edit (generated)

`home\*`, `library\*`, `site-masters\mfl-home-redesign-v1.html`,
`site-masters\mdhs-library-page.html`.

## Notes

- Background must stay as `.bg-photo` / `.bg-scrim` fixed divs. Carrd overrides
  `body::before/after`, which made the dark background fade out after ~2s.
- `tools\build-combined.ps1` is parked (one-page merge experiment, rejected).
- Full context: `JC Website\files\20-HANDOFF-2026-07-19-LIVE-SITE.md`.