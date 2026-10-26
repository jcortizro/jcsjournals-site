# THE ONE COMMAND. Rebuilds every page that is live today and writes the files the Carrd embeds fetch.
# After this: git add -A; git commit; git push  (the loaders read raw.githubusercontent, fresh within ~5 minutes).
#
# WHAT IS LIVE (measured 2026-10-26) AND WHAT BUILDS IT
#   jcsjournals.com ....... jcj\        = byte copy of td101page\ (tools\build-td101-page.py, then the copy below)
#   td101.carrd.co ........ td101page\  tools\build-td101-page.py, from src\td101-page\
#   freelibrary.carrd.co .. library\    build-library-page.ps1 + split-library.ps1 (the split adds the site menu)
#   freerecipes.carrd.co .. recipebook\index.html, generated on JC's other machine (export_to_site.py); this
#                           build only re-applies the site menu (tools\add-site-nav.py recipebook)
#   home\ ................. the old landing page; no site above loads it, rebuilt here as before
# All four live sites wear ONE menu, written once in tools\site_nav.py. tools\check-site-nav.py, the last step,
# fails this build if any page is missing it, carries a stale copy, or gets the links out of order.
#
# REMOVED ON 2026-10-26, ON PURPOSE. Do not run these four scripts:
#   build-jcj-page.ps1 + split-jcj.ps1 rebuilt jcj\ from the OLD hub master. Since 25 Oct 2026 jcj\ is the TD101
#     course page, so running them would silently replace the live jcsjournals.com page with the old hub.
#     (split-jcj.ps1 now refuses to run.)
#   build-signup-page.ps1 + split-signup.ps1 built the old td101.carrd.co waitlist (signup\). td101.carrd.co now
#     loads td101page\, so they rebuild a page no live site shows.
$ErrorActionPreference = "Stop"
$repo = "C:\Users\taino\jcsjournals-site"

& "$repo\tools\build-home-page.ps1"
& "$repo\tools\split-home.ps1"

& "$repo\tools\build-library-page.ps1"
& "$repo\tools\split-library.ps1"

& py -3.12 -X utf8 "$repo\tools\build-td101-page.py"
if ($LASTEXITCODE -ne 0) { throw "build-all: build-td101-page.py refused (exit $LASTEXITCODE); nothing copied to jcj\" }
foreach ($f in @("jcj.html", "jcj.css", "jcj.js")) {
  Copy-Item -LiteralPath "$repo\td101page\$f" -Destination "$repo\jcj\$f" -Force
}

& py -3.12 "$repo\tools\add-site-nav.py" recipebook
if ($LASTEXITCODE -ne 0) { throw "build-all: add-site-nav.py recipebook failed (exit $LASTEXITCODE)" }

& py -3.12 "$repo\tools\check-site-nav.py"
if ($LASTEXITCODE -ne 0) { throw "build-all: check-site-nav.py failed, a page does not carry the shared menu; do not push" }
Write-Output "BUILD ALL OK"
