# jcsjournals-site

Code for JC's live website. Two Carrd pages, each holding one small Embed(Code)
snippet that loads the real page from **raw.githubusercontent.com** (not jsDelivr —
its cache served stale files). Push here and the live pages update in ~5 minutes.
JC never re-pastes the snippets.

| Page | Live | Snippet |
|---|---|---|
| Landing (Free/Paid) | https://td101landing.carrd.co/ | `carrd-embed-home.html` |
| Library | https://td101library.carrd.co/ | `carrd-embed-library.html` |

## Build

    tools\build-all.ps1      # then: git add -A; git commit; git push

## Edit these (sources)

- `src\home.part.html` — the landing page AND the shared shell (background,
  header, dropdown, buttons). The library page is generated from this file, so
  shell edits hit both pages.
- `site-masters\mdhs-v4-final.html` (on D:) — the library's copy master: JC's
  locked article text + library component CSS/JS.
- `tools\urls.ps1` — the two page URLs. **Changing a domain = edit here, build, push.**
- `src\` — foliage.jpg + the embedded font CSS.

## Never hand-edit (generated)

`home\*`, `library\*`, `site-masters\mfl-home-redesign-v1.html`,
`site-masters\mdhs-library-page.html`.

## Notes

- Background must stay as `.bg-photo` / `.bg-scrim` fixed divs. Carrd overrides
  `body::before/after`, which made the dark background fade out after ~2s.
- `tools\build-combined.ps1` is parked (one-page merge experiment, rejected).
- Full context: `JC Website\files\20-HANDOFF-2026-07-19-LIVE-SITE.md`.