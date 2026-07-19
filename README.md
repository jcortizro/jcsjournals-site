# jcsjournals-site

Hosted code for the jcsjournals.com rebuild (Carrd + GitHub + jsDelivr CDN).

Carrd stays the host/domain/shell. Each Carrd page holds ONE small **Embed (Code)**
element; the heavy page code (CSS/HTML/JS) lives here and is served free via jsDelivr.

## Pages

| Page | Files | Carrd snippet |
|---|---|---|
| Library ("The Diet") | `library/library.css` · `library/library.html` · `library/library.js` | `carrd-embed-library.html` |
| Home (Free/Paid services, mockup) | `home/home.css` · `home/home.html` · `home/home.js` | `carrd-embed-home.html` |

Source of truth for content: the site-masters in
`D:\00. MUCUS-FREE LIFE\01. Operations\02. Working Procedures\Claude SOPs\00. JC Brand\JC Website\site-masters\`.
Edit the master, re-split, push here.

## Updating a live page

1. Edit the files, commit, push to `main`.
2. jsDelivr caches `@main` for ~12 h. Force-refresh with:
   `https://purge.jsdelivr.net/gh/jcortizro/jcsjournals-site@main/library/library.css`
   (repeat per file). The Carrd embed never needs re-pasting.

## Notes

- Fonts (Raleway / Source Sans Pro) are embedded in `library.css` as data URIs —
  no Google Fonts dependency, identical rendering everywhere.
- `library.html` is body markup only (no `<html>/<head>`); the loader injects it and
  hides the Carrd page's own content for a full-page takeover.
- The "My Content & Socials" button currently points at the home-page mockup artifact;
  repoint to the real home page at production rollout, along with the `#td101` links.
