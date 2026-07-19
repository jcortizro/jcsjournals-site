# Builds the COMBINED home page (home mockup + full library + FREE dropdown nav)
# into home/{home.css,home.html,home.js} (served by carrd-embed-home.html) and a
# single-file master for the artifact preview.
# Inputs: the repo's current home/* (from split-home.ps1) and library/* (from split-library.ps1).
$repo = "C:\Users\taino\jcsjournals-site"
$mastersDir = "D:\00. MUCUS-FREE LIFE\01. Operations\02. Working Procedures\Claude SOPs\00. JC Brand\JC Website\site-masters"
$enc = New-Object System.Text.UTF8Encoding($false)

$homeCss  = [System.IO.File]::ReadAllText("$repo\home\home.css")
$homeHtml = [System.IO.File]::ReadAllText("$repo\home\home.html")
$homeJs   = [System.IO.File]::ReadAllText("$repo\home\home.js")
$libCssLines = [System.IO.File]::ReadAllLines("$repo\library\library.css")
$libHtmlLines = [System.IO.File]::ReadAllLines("$repo\library\library.html")
$libJs    = [System.IO.File]::ReadAllText("$repo\library\library.js")

if ($homeHtml.Contains('id="library-sect"')) { throw "home.html already contains the combined build; re-run split-home.ps1 first" }

# ---- library CSS: drop fonts/root/body/bg (lines 1-21), then strip classes the home shell owns ----
$libCss = ($libCssLines[21..($libCssLines.Length-1)] -join "`n")
$killPatterns = @(
  '(?<![\w-])\.site-header[^{]*\{[^}]*\}',
  '(?<![\w-])\.hdr-in[^{]*\{[^}]*\}',
  '(?<![\w-])\.wordmark[^{]*\{[^}]*\}',
  '(?<![\w-])\.nav\{[^}]*\}',
  '(?<![\w-])\.hero[^{]*\{[^}]*\}',
  '(?<![\w-])\.lede[^{]*\{[^}]*\}',
  '(?<![\w-])\.eyebrow[^{]*\{[^}]*\}',
  '(?<![\w-])\.u\{[^}]*\}',
  '(?<![\w-])\.wrap\{[^}]*\}',
  '(?<![\w-])\.price\{[^}]*\}'
)
foreach ($p in $killPatterns) { $libCss = [regex]::Replace($libCss, $p, '') }
# tokens the library components use that the home :root no longer defines
$compat = ':root{--grad-green:linear-gradient(45deg,rgb(8,41,15) 0%,rgba(138,186,115,.12) 100%);--grad-green-lite:linear-gradient(45deg,rgba(18,58,29,.85) 0%,rgba(138,186,115,.05) 100%);--grad-blue:linear-gradient(45deg,rgb(5,57,240) 0%,rgba(8,183,207,.14) 100%);--grad-purple:linear-gradient(45deg,rgb(134,0,156) 0%,rgba(66,0,150,.14) 100%);--tier-green:#7ECB82;--tier-gold:#EBC64B;--tier-red:#E97676;--panel2:rgba(20,20,20,.66)}'
$combinedCss = $homeCss + "`n/* ==== LIBRARY (merged) ==== */`n" + $compat + "`n" + $libCss

# ---- dropdown graft: library header nav-item (lines 5-20) becomes the FREE dropdown ----
$dd = ($libHtmlLines[4..19] -join "`n")
$dd = $dd.Replace('<button class="nav-btn active" id="dietBtn"', '<button class="nav-btn" id="dietBtn"')
$dd = $dd.Replace('>Education <span class="chev">', '>Free <span class="chev">')
$dd = $dd.Replace('<div class="dropdown" id="dietDD">', ('<div class="dropdown" id="dietDD">' + "`n" + '          <a class="dd-go" href="#free" data-close-dd>&#9733; Start here: the four free resources</a>'))
$combinedHtml = $homeHtml.Replace('      <a class="free-lnk" href="#free">Free</a>', $dd)
if ($combinedHtml -eq $homeHtml) { throw "free-lnk anchor not found for dropdown graft" }

# ---- library body: from <section id="library"> through end of main, + legal dialog ----
$startIdx = -1; $endIdx = -1; $dialogIdx = -1
for ($i = 0; $i -lt $libHtmlLines.Length; $i++) {
  if ($startIdx -lt 0 -and $libHtmlLines[$i] -match 'class="section" id="library"') { $startIdx = $i }
  if ($libHtmlLines[$i].Trim() -eq '</main>') { $endIdx = $i }
  if ($libHtmlLines[$i] -match '<dialog id="legalModal"') { $dialogIdx = $i }
}
if ($startIdx -lt 0 -or $endIdx -lt 0 -or $dialogIdx -lt 0) { throw "library markers not found: $startIdx / $endIdx / $dialogIdx" }
$libBody = ($libHtmlLines[$startIdx..($endIdx-1)] -join "`n")
$libDialog = $libHtmlLines[$dialogIdx]

$libSection = @"
  <!-- THE LIBRARY (merged from library/library.html · edit the library master, re-split, re-run build-combined) -->
  <section id="library-sect">
    <div class="sect-head">
      <p class="sect-kicker free-k">The Library</p>
      <h2>The library, on this same page</h2>
      <p class="sect-lede">A basic overview of the Mucusless Diet Healing System: the what, the why, the how, and the full FAQ. Pick a topic below, or use the Free menu at the top; each one opens right where it is.</p>
    </div>
  </section>
$libBody
$libDialog
"@
$aboutComment = '  <!-- ABOUT US'
$pos = $combinedHtml.IndexOf($aboutComment)
if ($pos -lt 0) { throw "about-us comment anchor not found" }
$combinedHtml = $combinedHtml.Substring(0, $pos) + $libSection + "`n" + $combinedHtml.Substring($pos)

# ---- JS: home bindings + library engine ----
$combinedJs = $homeJs + "`n/* ==== LIBRARY (merged) ==== */`n" + $libJs

[System.IO.File]::WriteAllText("$repo\home\home.css",  $combinedCss,  $enc)
[System.IO.File]::WriteAllText("$repo\home\home.html", $combinedHtml, $enc)
[System.IO.File]::WriteAllText("$repo\home\home.js",   $combinedJs,   $enc)

# ---- single-file master for the artifact preview ----
$single = '<meta charset="utf-8">' + "`n" +
  '<meta name="viewport" content="width=device-width, initial-scale=1">' + "`n" +
  '<meta name="color-scheme" content="dark">' + "`n" +
  '<title>Free Education · The Mucusless Diet Healing System</title>' + "`n" +
  "<style>`n" + $combinedCss + "`n</style>`n" + $combinedHtml + "`n<script>`n" + $combinedJs + "`n</script>`n"
[System.IO.File]::WriteAllText("$mastersDir\mfl-home-combined.html", $single, $enc)

Write-Output ("combined css chars: " + $combinedCss.Length)
Write-Output ("combined html chars: " + $combinedHtml.Length)
Write-Output ("combined js chars: " + $combinedJs.Length)
Write-Output "combined build OK"
