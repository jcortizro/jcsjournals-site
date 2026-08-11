# Generates the LIBRARY page FROM the landing page's shell (JC's directive 7/19:
# "copy the landing page code, take out the landing content, put the library content in").
# Shell (tokens/bg/scrim/header/footer/mnav/JS) comes verbatim from mfl-redesign.part.html;
# content (hero copy, topic bars, dialog) is extracted from mdhs-v4-final.html (the copy
# source of truth); component CSS/JS come from the split library files with shell classes
# filtered out. Output: site-masters\mdhs-library-page.html (what split-library.ps1 serves).
$masters = "D:\00. MUCUS-FREE LIFE\01. Operations\02. Working Procedures\Claude SOPs\00. JC Brand\JC Website\site-masters"
$repo = "C:\Users\taino\jcsjournals-site"
. "$repo\tools\urls.ps1"
$landingUrl = $LandingUrl
$enc = New-Object System.Text.UTF8Encoding($false)

$part = [System.IO.File]::ReadAllText("$repo\src\home.part.html")
$content = [System.IO.File]::ReadAllText("$masters\mdhs-v4-final.html")
# components come from the COPY MASTER's own style/script blocks (stable source; the
# repo library/* files are generated FROM this script's output and must not feed it)
$mLines = [System.IO.File]::ReadAllLines("$masters\mdhs-v4-final.html")
$styleStart = -1; $styleEnd = -1; $scriptStart = -1; $scriptEnd = -1
for ($i = 0; $i -lt $mLines.Length; $i++) {
  $l = $mLines[$i].Trim()
  if ($l -eq '<style>' -and $styleStart -lt 0) { $styleStart = $i }
  elseif ($l -eq '</style>' -and $styleEnd -lt 0) { $styleEnd = $i }
  elseif ($l -eq '<script>' -and $scriptStart -lt 0) { $scriptStart = $i }
  elseif ($l -eq '</script>') { $scriptEnd = $i }
}
if ($styleStart -lt 0 -or $styleEnd -lt 0 -or $scriptStart -lt 0 -or $scriptEnd -lt 0) { throw "master block markers not found" }
$libCssLines = $mLines[($styleStart+1)..($styleEnd-1)]
$libJsLines = $mLines[($scriptStart+1)..($scriptEnd-1)]

# ---- extract library content from the copy master ----
$ledeM = [regex]::Match($content, '<p class="lede">This information[\s\S]*?</p>')
if (-not $ledeM.Success) { throw "hero lede not found" }
$heroLede = $ledeM.Value
$secStart = $content.IndexOf('<section class="section" id="library">')
$mainEnd = $content.IndexOf('</main>')
if ($secStart -lt 0 -or $mainEnd -lt 0) { throw "library section markers not found" }
$libSection = $content.Substring($secStart, $mainEnd - $secStart)
$libSection = [regex]::Replace($libSection, '<section class="section" id="library">\s*<div class="wrap">', '<section id="library">')
$libSection = [regex]::Replace($libSection, '</div>\s*</section>\s*$', '</section>')
$dialogM = [regex]::Match($content, '<dialog id="legalModal">.*')
if (-not $dialogM.Success) { throw "dialog not found" }
$dialog = ($dialogM.Value -split "`n")[0]

$libHero = @"
  <div class="hero">
    <p class="eyebrow">The Library &middot; Free &middot; No Email Signup Required</p>
    <h1>Mucus-Free<br>Made Simple</h1>
    $heroLede
    <p class="lede">Pick a topic below; each one opens right where it is.</p>
    <a class="vidrow" href="https://youtu.be/Djygxncc58I" target="_blank" rel="noopener">
      <span class="vp" aria-hidden="true"></span>
      <span><span class="vt">What is the Mucusless Diet Healing System?</span><span class="vn">Watch the video first</span></span>
    </a>
  </div>
"@

# ---- swap the landing's main content for the library content ----
$mainMarker = '<main class="wrap" id="top">'
$mainStart = $part.IndexOf($mainMarker) + $mainMarker.Length
$footerStart = $part.IndexOf('  <footer>')
if ($mainStart -lt $mainMarker.Length -or $footerStart -lt 0) { throw "main/footer markers not found in part" }
$page = $part.Substring(0, $mainStart) + "`n`n" + $libHero + "`n" + $libSection + "`n" + $dialog + "`n`n" + $part.Substring($footerStart)

# ---- component CSS from the split library, shell classes filtered out ----
$libCss = ($libCssLines | Where-Object { $_ -notmatch '^@font-face|^:root|^\*\{|^html|^body|^a\{|^button\{|^:focus-visible|^\.mock-note|^\.bg-photo|^\.bg-scrim|^main' }) -join "`n"
$killPatterns = @(
  '(?<![\w-])\.site-header[^{]*\{[^}]*\}','(?<![\w-])\.hdr-in[^{]*\{[^}]*\}','(?<![\w-])\.hnav[^{]*\{[^}]*\}',
  '(?<![\w-])\.nav-item[^{]*\{[^}]*\}','(?<![\w-])\.nav-btn[^{]*\{[^}]*\}','(?<![\w-])\.dropdown[^{]*\{[^}]*\}',
  '(?<![\w-])\.hero[^{]*\{[^}]*\}','(?<![\w-])\.eyebrow[^{]*\{[^}]*\}','(?<![\w-])\.lede[^{]*\{[^}]*\}',
  '(?<![\w-])\.accent-rule[^{]*\{[^}]*\}','(?<![\w-])\.u\{[^}]*\}','(?<![\w-])\.wrap\{[^}]*\}',
  '(?<![\w-])\.section[^{]*\{[^}]*\}','(?<![\w-])\.mock-note[^{]*\{[^}]*\}','(?<![\w-])\.mnav[^{]*\{[^}]*\}',
  '(?<![\w-])\.site-footer[^{]*\{[^}]*\}','(?<![\w-])\.foot-links[^{]*\{[^}]*\}','(?<![\w-])footer[^{]*\{[^}]*\}',
  '(?<![\w-])\.btn[^{]*\{[^}]*\}','(?<![\w-])\.vidrow[^{]*\{[^}]*\}','(?<![\w-])\.chip\{[^}]*\}',
  '(?<![\w-])\.dn\{[^}]*\}','(?<![\w-])h1\{[^}]*\}','(?<![\w-])h2\{[^}]*\}'
)
foreach ($p in $killPatterns) { $libCss = [regex]::Replace($libCss, $p, '') }
$compat = ':root{--gold:#E4BE3F;--dim2:rgba(255,255,255,.85);--tier-green:#7ECB82;--tier-gold:#EBC64B;--tier-red:#E97676;--grad-green:linear-gradient(45deg,rgb(8,41,15) 0%,rgba(138,186,115,.12) 100%)}'
$page = $page.Replace('</style>', ("/* ==== LIBRARY components ==== */`n" + $compat + "`n" + $libCss + "`n</style>"))

# ---- library engine JS (minus the shell dropdown code the landing already has) ----
$libJs = ($libJsLines | Where-Object { $_ -notmatch 'freeBtn|freeDD|hideNote' }) -join "`n"
$page = $page.Replace('</script>', ("`n/* ==== LIBRARY engine ==== */`n" + $libJs + "`n</script>"))

# ---- cross-page wiring: this page's shell links go to the real landing page ----
$page = $page.Replace('href="#free" data-close-dd>Transition Diet 101</a>', ('href="' + $landingUrl + '#free">Transition Diet 101</a>'))
$page = $page.Replace('<a href="__LIBURL__">The Library</a>', '<a href="#library" data-close-dd>The Library</a>')
# The recipe book is a REAL page now (2026-08-10), so its dropdown item goes
# straight there instead of to the parked landing.
$page = $page.Replace('href="#free" data-close-dd>The Recipe Book</a>', ('href="' + $RecipesUrl + '">The Recipe Book</a>'))
$page = $page.Replace('href="#free" data-close-dd>The Book + Mind Maps</a>', ('href="' + $landingUrl + '#free">The Book + Mind Maps</a>'))
$page = $page.Replace('<a class="h-paid" href="#paid">Paid</a>', ('<a class="h-paid" href="' + $landingUrl + '#paid">Paid</a>'))
$page = $page.Replace('<a class="h-home" href="#top">Home</a>', ('<a class="h-home" href="' + $landingUrl + '">Home</a>'))
$page = $page.Replace('<a class="mf" href="#free">Free</a>', '<a class="mf" href="#library">Free</a>')
$page = $page.Replace('<a class="mp" href="#paid">Paid</a>', ('<a class="mp" href="' + $landingUrl + '#paid">Paid</a>'))
# content + engine links that still point at the old artifact preview -> real landing
$page = $page.Replace('https://claude.ai/code/artifact/f26c6153-1077-44fe-8d03-fc3dea7dcf28', $landingUrl.TrimEnd('/'))
$page = $page.Replace($landingUrl.TrimEnd('/') + '#', $landingUrl + '#')
# mock-note text for this page
$page = $page.Replace("Claude's take after the design critique: one job per screen, the fork as the centerpiece, real CTAs, no carousels. All copy placeholder: JC owns every word.", "The Library, wearing the landing page's exact shell. All copy is JC's locked text.")
$page = $page.Replace('<title>Free Education · The Mucusless Diet Healing System</title>', '<title>The Library · The Mucusless Diet Healing System</title>')

# ---- assets ----
$assets = [System.IO.File]::ReadAllText("$repo\src\montserrat.css") + "`n" + [System.IO.File]::ReadAllText("$repo\src\source-sans-3.css")
$bg64 = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes("$repo\src\foliage.jpg"))
$page = $page.Replace('/*__ASSETS__*/', $assets).Replace('__BGIMG__', $bg64)
if ($page.Contains('__LIBURL__') -or $page.Contains('__BGIMG__')) { throw "unresolved tokens remain" }

# ---- ONE HEADER ACROSS THE FAMILY (JC 2026-08-10) ----
# All three sites must look like one website, so the library wears the same
# wordmark + social icons header as jcsjournals.com. The old Home/Free/Paid
# dropdown it replaces was navigation; the dock bar below now carries that job.
# Done HERE, at the top of the chain, so the jcj page inherits it (that page is
# generated FROM this master) instead of each build repeating the swap.
$hdr = [System.IO.File]::ReadAllText("$repo\src\jcj-parts\new-header.html")
$n = ([regex]::Matches($page, '(?s)<header class="site-header">.*?</header>')).Count
if ($n -ne 1) { throw "build-library: expected 1 header, found $n" }
$page = [regex]::Replace($page, '(?s)<header class="site-header">.*?</header>', { param($m) $hdr })

# the dropdown's JS is now orphaned; drop it so it cannot throw on a missing node
$ddRx = "(?s)var freeBtn=document\.getElementById\('freeBtn'\).*?(?=document\.querySelectorAll\('\.more-btn'\))"
$n = ([regex]::Matches($page, $ddRx)).Count
if ($n -ne 1) { throw "build-library: expected 1 dropdown JS block, found $n" }
$page = [regex]::Replace($page, $ddRx, '')
Write-Output "  shared header + dropdown JS removed : ok"

# ---- THE DOCK BAR (shared with jcsjournals.com and the recipe book) ----
# One source in src\shared; this page just fills in its contact target, which
# lives on the hub. Guarded: each injection must land exactly once.
$dockHtml = [System.IO.File]::ReadAllText("$repo\src\shared\dock.html").Replace('__CONTACT__', 'https://jcsjournals.com/#work-with-us')
$dockCss  = [System.IO.File]::ReadAllText("$repo\src\shared\dock.css")
$dockJs   = [System.IO.File]::ReadAllText("$repo\src\shared\dock.js")
if ($dockHtml.Contains('__CONTACT__')) { throw "build-library: dock contact token unresolved" }

$headerCss = [System.IO.File]::ReadAllText("$repo\src\shared\header.css")
$n = ([regex]::Matches($page, '</style>')).Count
if ($n -ne 1) { throw "build-library: expected 1 </style>, found $n" }
$page = $page.Replace('</style>', ("/* ==== SHARED HEADER ==== */`n" + $headerCss + "`n/* ==== DOCK BAR ==== */`n" + $dockCss + "`n</style>"))

$n = ([regex]::Matches($page, '</script>')).Count
if ($n -ne 1) { throw "build-library: expected 1 </script>, found $n" }
$page = $page.Replace('</script>', ("`n/* ==== DOCK BAR ==== */`n" + $dockJs + "`n</script>"))

# The dock REPLACES the old mobile pill rather than sitting next to it. Remove
# the pill here, at the top of the chain, so the jcj page (which is generated
# FROM this master) inherits exactly one dock and never a duplicate.
$n = ([regex]::Matches($page, '(?s)<nav class="mnav"[^>]*>.*?</nav>')).Count
if ($n -ne 1) { throw "build-library: expected 1 mnav to remove, found $n" }
$page = [regex]::Replace($page, '(?s)<nav class="mnav"[^>]*>.*?</nav>', '')

$n = ([regex]::Matches($page, '  <footer>')).Count
if ($n -ne 1) { throw "build-library: expected 1 footer marker, found $n" }
$page = $page.Replace('  <footer>', ($dockHtml + "`n  <footer>"))

$n = ([regex]::Matches($page, '<nav class="dockbar"')).Count
if ($n -ne 1) { throw "build-library: expected exactly 1 dock, found $n" }
Write-Output "  mnav removed + dock bar injected : ok"

# Dead-subdomain guard (2026-08-10 rename): the old Carrd names must never ship.
if ($page -match 'td101landing|td101library') { throw "build-library: dead td101 subdomain reference remains" }

[System.IO.File]::WriteAllText("$masters\mdhs-library-page.html", $page, $enc)
Write-Output ("library page generated: " + (Get-Item "$masters\mdhs-library-page.html").Length + " bytes")
