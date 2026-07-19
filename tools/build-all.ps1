# THE ONE COMMAND. Rebuilds both pages from source and writes the files the
# Carrd embeds fetch. After this: git add -A; git commit; git push  (no purge —
# the loaders read raw.githubusercontent, which is fresh within ~5 minutes).
#
# SOURCES (edit these):
#   src\home.part.html ............ landing page markup/CSS/JS + the shared shell
#   site-masters\mdhs-v4-final.html  library COPY master (JC's locked text)
#   tools\urls.ps1 ................ the two page URLs
# OUTPUTS (never hand-edit):
#   site-masters\mfl-home-redesign-v1.html, site-masters\mdhs-library-page.html
#   home\*, library\*
$repo = "C:\Users\taino\jcsjournals-site"
& "$repo\tools\build-home-page.ps1"
& "$repo\tools\split-home.ps1"
& "$repo\tools\build-library-page.ps1"
& "$repo\tools\split-library.ps1"
Write-Output "BUILD ALL OK"
