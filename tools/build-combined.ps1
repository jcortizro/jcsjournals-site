# Builds the ONE-CODE app: home + full library in a single embed, as TWO SWITCHED
# VIEWS (not one scroll). The Free dropdown swaps to the library view and opens the
# chosen topic; "Home" swaps back. Writes home/{home.css,home.html,home.js} (served
# by carrd-embed-home.html) + a single-file master for the artifact preview.
# Inputs: repo home/* (from split-home.ps1, home-only) and library/* (from split-library.ps1).
$repo = "C:\Users\taino\jcsjournals-site"
$mastersDir = "D:\00. MUCUS-FREE LIFE\01. Operations\02. Working Procedures\Claude SOPs\00. JC Brand\JC Website\site-masters"
$enc = New-Object System.Text.UTF8Encoding($false)

$homeCss  = [System.IO.File]::ReadAllText("$repo\home\home.css")
$homeHtml = [System.IO.File]::ReadAllText("$repo\home\home.html")
$homeJsLines = [System.IO.File]::ReadAllLines("$repo\home\home.js")
$libCssLines = [System.IO.File]::ReadAllLines("$repo\library\library.css")
$libHtmlLines = [System.IO.File]::ReadAllLines("$repo\library\library.html")
$libJs    = [System.IO.File]::ReadAllText("$repo\library\library.js")

if ($homeHtml.Contains('id="view-library"')) { throw "home.html already contains the one-code build; re-run split-home.ps1 first" }

# ---- library CSS: drop fonts/root/body/bg (lines 1-21), then strip classes the home shell owns ----
$libCss = ($libCssLines[21..($libCssLines.Length-1)] -join "`n")
$killPatterns = @(
  '(?<![\w-])\.site-header[^{]*\{[^}]*\}',
  '(?<![\w-])\.hdr-in[^{]*\{[^}]*\}',
  '(?<![\w-])\.wordmark[^{]*\{[^}]*\}',
  '(?<![\w-])\.home-lnk[^{]*\{[^}]*\}',
  '(?<![\w-])\.nav\{[^}]*\}',
  '(?<![\w-])\.nav-btn[^{]*\{[^}]*\}',
  '(?<![\w-])\.nav-item[^{]*\{[^}]*\}',
  '(?<![\w-])\.dropdown[^{]*\{[^}]*\}',
  '(?<![\w-])\.dd-cat[^{]*\{[^}]*\}',
  '(?<![\w-])\.dd-subs[^{]*\{[^}]*\}',
  '(?<![\w-])\.dd-go[^{]*\{[^}]*\}',
  '(?<![\w-])\.dd-note[^{]*\{[^}]*\}',
  '(?<![\w-])\.hero[^{]*\{[^}]*\}',
  '(?<![\w-])\.lede[^{]*\{[^}]*\}',
  '(?<![\w-])\.eyebrow[^{]*\{[^}]*\}',
  '(?<![\w-])\.u\{[^}]*\}',
  '(?<![\w-])\.wrap\{[^}]*\}',
  '(?<![\w-])\.price\{[^}]*\}'
)
foreach ($p in $killPatterns) { $libCss = [regex]::Replace($libCss, $p, '') }
$compat = ':root{--grad-green:linear-gradient(45deg,rgb(8,41,15) 0%,rgba(138,186,115,.12) 100%);--grad-green-lite:linear-gradient(45deg,rgba(18,58,29,.85) 0%,rgba(62,122,76,.05) 100%);--grad-blue:linear-gradient(45deg,rgb(5,57,240) 0%,rgba(8,183,207,.14) 100%);--grad-purple:linear-gradient(45deg,rgb(134,0,156) 0%,rgba(66,0,150,.14) 100%);--tier-green:#7ECB82;--tier-gold:#EBC64B;--tier-red:#E97676}'
$combinedCss = $homeCss + "`n/* ==== LIBRARY (merged view) ==== */`n" + $compat + "`n" + $libCss

# ---- replace the home cross-page dropdown with the library's in-document dropdown ----
$navStart = $homeHtml.IndexOf('<div class="nav-item">')
$navEnd = $homeHtml.IndexOf('<a class="paid-lnk"')
if ($navStart -lt 0 -or $navEnd -lt 0 -or $navEnd -le $navStart) { throw "nav-item / paid-lnk markers not found" }
$dd = ($libHtmlLines[4..19] -join "`n")
$dd = $dd.Replace('<button class="nav-btn active" id="dietBtn"', '<button class="nav-btn" id="dietBtn"')
$dd = $dd.Replace('>Education <span class="chev">', '>Free <span class="chev">')
$dd = $dd.Replace('<div class="dropdown" id="dietDD">', ('<div class="dropdown" id="dietDD">' + "`n" + '          <a href="#free" data-close-dd>The four free resources</a>'))
$combinedHtml = $homeHtml.Substring(0, $navStart) + $dd + "`n      " + $homeHtml.Substring($navEnd)

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

# ---- wrap the two views ----
$mainOpen = '<main class="wrap" id="top">'
$pos = $combinedHtml.IndexOf($mainOpen)
if ($pos -lt 0) { throw "main marker not found" }
$combinedHtml = $combinedHtml.Substring(0, $pos + $mainOpen.Length) + "`n<div id=`"view-home`">" + $combinedHtml.Substring($pos + $mainOpen.Length)

$libView = @"
</div><!-- /view-home -->
  <div id="view-library" hidden>
  <!-- THE LIBRARY VIEW (merged from library/library.html · edit the library master, re-split, re-run build-combined) -->
  <section id="library-sect">
    <div class="sect-head">
      <p class="sect-kicker free-k">The Library</p>
      <h2>A basic overview of the system</h2>
      <p class="sect-lede">The what, the why, the how, and the full FAQ. Pick a topic below, or use the Free menu at the top; each one opens right where it is.</p>
    </div>
  </section>
$libBody
$libDialog
  </div><!-- /view-library -->
"@
$aboutComment = '  <!-- ABOUT US'
$pos = $combinedHtml.IndexOf($aboutComment)
if ($pos -lt 0) { throw "about-us comment anchor not found" }
$combinedHtml = $combinedHtml.Substring(0, $pos) + $libView + "`n" + $combinedHtml.Substring($pos)

# ---- JS: home bindings (minus the old cross-page dropdown code) + view router + library engine ----
$homeJs = (($homeJsLines | Where-Object { $_ -notmatch 'freeDD' }) -join "`n")
$viewJs = @'
/* ==== view router (one code, two pages) ==== */
function showView(v){var h=document.getElementById('view-home'),l=document.getElementById('view-library');var lib=(v==='library');h.hidden=lib;l.hidden=!lib;}
function viewOf(id){var el=document.getElementById(id);if(!el)return null;return document.getElementById('view-library').contains(el)?'library':'home';}
document.addEventListener('click',function(e){var a=e.target.closest('a[href^="#"],[data-open]');if(!a)return;var id=(a.dataset&&a.dataset.open)?a.dataset.open:(a.getAttribute('href')||'').slice(1);if(!id)return;var v=viewOf(id);if(!v)return;var cur=document.getElementById('view-library').hidden?'home':'library';if(v!==cur){showView(v);window.scrollTo(0,0);}},true);
(function(){var id=location.hash.slice(1);if(id&&viewOf(id)==='library'){showView('library');}})();
'@
$combinedJs = $homeJs + "`n" + $viewJs + "`n/* ==== LIBRARY engine ==== */`n" + $libJs

[System.IO.File]::WriteAllText("$repo\home\home.css",  $combinedCss,  $enc)
[System.IO.File]::WriteAllText("$repo\home\home.html", $combinedHtml, $enc)
[System.IO.File]::WriteAllText("$repo\home\home.js",   $combinedJs,   $enc)

$single = '<meta charset="utf-8">' + "`n" +
  '<meta name="viewport" content="width=device-width, initial-scale=1">' + "`n" +
  '<meta name="color-scheme" content="dark">' + "`n" +
  '<title>Free Education · The Mucusless Diet Healing System</title>' + "`n" +
  "<style>`n" + $combinedCss + "`n</style>`n" + $combinedHtml + "`n<script>`n" + $combinedJs + "`n</script>`n"
[System.IO.File]::WriteAllText("$mastersDir\mfl-home-combined.html", $single, $enc)

Write-Output ("combined css chars: " + $combinedCss.Length)
Write-Output ("combined html chars: " + $combinedHtml.Length)
Write-Output ("combined js chars: " + $combinedJs.Length)
Write-Output "one-code build OK"
