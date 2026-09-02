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
$compat = $compat + 'a.tdwatch::after{content:"WATCH IT FREE";font-family:var(--body);font-weight:600;font-size:.68rem;letter-spacing:.6px;text-transform:uppercase;color:var(--dim);background:rgba(255,255,255,.06);border:1px solid var(--hair-strong);border-radius:99px;padding:4px 9px;margin-left:8px;white-space:nowrap;display:inline-block;vertical-align:baseline;text-decoration:none}a.tdwatch:hover::after{border-color:var(--gold);filter:brightness(1.35)}'
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

# ---- LANDINGS MUST BE INSTANT, NOT SMOOTH ----
# Arriving at freelibrary.carrd.co/#greenjuice opened the right topic but did
# not move the page: measured scrollY 0 with the target 2086px down. Carrd
# interrupts a smooth scroll over that distance. Instant lands every time, and
# the css scroll-behavior is forced off around it because 'auto' defers to it.
$smooth = "window.scrollTo({top:y,behavior:'smooth'})"
$instant = "(function(){var de=document.documentElement,p=de.style.scrollBehavior;de.style.scrollBehavior='auto';window.scrollTo(0,y);de.style.scrollBehavior=p;})()"
$n = ([regex]::Matches($page, [regex]::Escape($smooth))).Count
if ($n -ne 3) { throw "build-library: expected 3 smooth scrollTo calls, found $n" }
$page = $page.Replace($smooth, $instant)
Write-Output "  landings forced instant : 3 ok"

# ---- CROSS LINKS INTO THE FREE RECIPE BOOK (JC 2026-08-10) ----
# "the library needs those free recipe book links where it makes sense", and
# clicking one must land the reader on that exact spread. Each note is added
# right under the existing visual-note in the same topic, and reuses the
# visual-note class verbatim, so the formatting is the page's own proven block
# and cannot drift. Its links already render gold (.visual-note a{color:gold}).
# Anchors are matched on pure ASCII phrases because PS 5.1 reads this file as
# ANSI and an emoji literal here would corrupt; the marker is built by code point.
$salad = [char]::ConvertFromUtf32(0x1F957)

function AddRecipeNote([string]$label, [string]$uniquePhrase, [string]$inner) {
  $rx = '<div class="visual-note">(?:(?!</div>).)*?' + [regex]::Escape($uniquePhrase) + '(?:(?!</div>).)*?</div>'
  $m = [regex]::Matches($script:page, $rx, 'Singleline')
  if ($m.Count -ne 1) { throw "build-library: recipe note '$label' anchor matched $($m.Count), expected 1" }
  $note = '<div class="visual-note"><span class="vv" aria-hidden="true">' + $script:salad + '</span><span>' + $inner + '</span></div>'
  $script:page = $script:page.Replace($m[0].Value, $m[0].Value + $note)
  Write-Output "  recipe note [$label] : ok"
}

# Deep links into the book use ?r= rather than #, because Carrd wipes the hash
# on that site before the book's script can read it (measured: #r08 arrived
# with an empty hash and no scroll). The query string survives.
$bk = $RecipesUrl.TrimEnd('/') + '/?r='
AddRecipeNote 'fruit' 'created by yours truly.' `
  ("Want the meals themselves? The <a href=`"${bk}r09`">Mono Fruit Meal</a> and <a href=`"${bk}r10`">Dried Fruit Followed by Juicy Fruit</a> are written out step by step in the free recipe book.")
AddRecipeNote 'veg' 'of the whole vegetable meal, built visually' `
  ("The salad bases that put this into practice start with the <a href=`"${bk}r01`">Carrot-Cabbage Coleslaw</a> in the free recipe book.")
AddRecipeNote 'howtoeat' 'you can also download the free infographic guide' `
  ("For a full vegetable meal built exactly this way, see the <a href=`"${bk}r02`">Kale and Spinach Minced Salad</a> in the free recipe book.")
AddRecipeNote 'greenjuice' 'green juice, check out' `
  ("Both green juices are written out in the free recipe book: <a href=`"${bk}r07`">my green juice</a> and the <a href=`"${bk}r08`">Soothing Green Juice</a>.")
AddRecipeNote 'timing' 'a stunning visual infographic of this information' `
  ("The two-course fruit meal this timing is built around is the <a href=`"${bk}r10`">Dried Fruit Followed by Juicy Fruit</a> in the free recipe book.")

# ---- THE PARKED COURSE (2026-08-10) ----
# Transition Diet 101 does not exist yet, and the page these links used to
# reach (td101landing) is gone. Left alone they point at an anchor that is not
# there, so the reader lands nowhere. Park them exactly as the hub already
# does: de-linked, still readable. Done here so the jcj page inherits it.
$greenBtn = '<a class="btn green" class="tdlink" href="' + $landingUrl + '#free">What Is Transition Diet 101?</a>'
# ---- THE COURSE IS NO LONGER A DEAD END (2026-08-11) ----
# The course still does not exist, but the WAITLIST does, so these stop being
# parked ghosts and become a real action: leave your name, get in the moment it
# opens. JC, 2026-08-11: "I'm cool with the library getting a little bit more
# text because that's fine, that's definitely a reader's haven", so unlike the
# recipe book this side carries a full sentence of promise, not just a chip.
$n = ([regex]::Matches($page, [regex]::Escape($greenBtn))).Count
if ($n -ne 1) { throw "build-library: expected 1 green course button, found $n" }
# 2026-09-02, JC: the course is OPEN, everything relabels to "Get Access".
$page = $page.Replace($greenBtn, '<a class="btn green" href="' + $SignupUrl + '">Get Access</a>')

# JC's own "Make My Free Account" placeholder. There are no accounts to make and
# the waitlist button beside it already carries the action, so two buttons to
# one destination would just be noise. Remove it rather than duplicate the CTA.
$acct = '<span class="btn ghost">Make My Free Account <span class="chip">soon</span></span>'
$n = ([regex]::Matches($page, [regex]::Escape($acct))).Count
if ($n -ne 1) { throw "build-library: expected 1 'Make My Free Account' ghost, found $n" }
$page = $page.Replace($acct, '')

# The promise, in the paragraph that already sends the reader to the course.
$tail = 'apply this information lives.</p>'
$n = ([regex]::Matches($page, [regex]::Escape($tail))).Count
if ($n -ne 1) { throw "build-library: expected 1 course paragraph tail, found $n" }
$page = $page.Replace($tail, 'apply this information lives. It is free and it is open right now: ' +
  'leave your email below and you will be sent access, no payment and no catch.</p>')

$n = ([regex]::Matches($page, '<a class="tdlink" href="[^"]*">(.*?)</a>')).Count
if ($n -ne 14) { throw "build-library: expected 14 tdlinks, found $n" }
# REVERSED 2026-08-21 ON JC'S ORDER. These 14 were switched off on 2026-08-11
# because "14 links to one page reads as spam". He overruled it: "the library
# needs to have every part that the Transition Diet 101 course can be mentioned
# and have a clickable link where people are sent to it... We've been losing so
# many people!" The anti-spam control is NOT fewer links, it is that these are
# inline TEXT links (white, bold, gold underline, already styled by
# .acc-body a.tdlink) and there is still exactly ONE button on the page.
$page = [regex]::Replace($page, '<a class="tdlink" href="[^"]*">(.*?)</a>', ('<a class="tdlink" href="' + $SignupUrl + '">$1</a>'))

$n = ([regex]::Matches($page, '<a class="tdlink" href="' + [regex]::Escape($SignupUrl) + '">')).Count
if ($n -ne 14) { throw "build-library: expected 14 live tdlinks after the swap, found $n" }
if ([regex]::Matches($page, '<span class="tdlink">').Count -ne 0) { throw "build-library: a dead tdlink span survived" }
Write-Output "  14 inline course links LIVE : ok"

# ---- REGISTER 2: the five video promises carry a chip (2026-08-21) ----
# Five of the fourteen do not pitch the course, they promise a specific video or
# infographic that lives inside it. That is the highest intent moment on the
# page, so the chip names the ASSET, not the course. Detected by the film
# clapper glyph that already opens each of those notes, so a copy edit that adds
# or removes a video promise fails this build loudly instead of drifting.
# Built by code point: PS 5.1 reads this file as ANSI and an emoji literal
# here would corrupt (same reason as the salad marker above).
$film = [char]::ConvertFromUtf32(0x1F3AC)
# NOTE 2026-08-21: bounded by </div>, not </span>. Measured markup: the glyph
# sits inside its OWN icon-only span (<span class="vv">[glyph]</span>) that
# closes immediately, so a </span> boundary trips before ever reaching the
# target anchor. The real scope of one visual-note is its enclosing </div>.
$watchRx = '(?s)' + [regex]::Escape($film) + '(?:(?!</div>).)*?<a class="tdlink"'
$n = ([regex]::Matches($page, $watchRx)).Count
if ($n -ne 5) { throw "build-library: expected 5 watch-register mentions, found $n" }
$page = [regex]::Replace($page, $watchRx, { param($m) $m.Value.Replace('<a class="tdlink"', '<a class="tdlink tdwatch"') })
$n = ([regex]::Matches($page, 'class="tdlink tdwatch"')).Count
if ($n -ne 5) { throw "build-library: expected 5 tdwatch links, found $n" }
Write-Output "  5 watch chips : ok"
Write-Output "  course CTA live + account ghost removed + 14 mentions plain : ok"

# ---- ONE FOOTER ACROSS THE FAMILY ----
# The shell still carried the design-proposal footer ("Branding TBD, Redesign
# proposal..."), which was shipping on the live library page. Same real footer
# as the hub, applied here so the jcj page inherits it.
$ftr = [System.IO.File]::ReadAllText("$repo\src\jcj-parts\new-footer.html")
$fm = [regex]::Matches($page, '(?s)<footer>.*?</footer>')
if ($fm.Count -ne 1) { throw "build-library: expected 1 footer, found $($fm.Count)" }
$page = $page.Replace($fm[0].Value, $ftr)
# The design-proposal scaffolding note ships too: its CSS is filtered out of
# this page, so the text renders raw at the bottom of a live site. Remove the
# element, not just its wording.
$mn = [regex]::Matches($page, '(?s)<div class="mock-note">.*?</div>')
if ($mn.Count -ne 1) { throw "build-library: expected 1 mock-note, found $($mn.Count)" }
$page = $page.Replace($mn[0].Value, '')
# Guard the VISIBLE mockup copy only. ("branding TBD" also appears in an HTML
# comment in the header, which the header swap below deletes anyway, and which
# a reader never sees. PS -match is case insensitive while [regex]::Matches is
# not, which is what made that comment look like a survivor.)
if (([string]$page) -match 'Redesign proposal|placeholder drafts he owns') { throw "build-library: mockup scaffolding survived" }
Write-Output "  shared footer + scaffolding removed : ok"

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
# One source in src\shared. ⛔ No Contact/Calendly item (removed 2026-08-25,
# JC): the dock must never carry a link to a booking/contact surface.
$dockHtml = [System.IO.File]::ReadAllText("$repo\src\shared\dock.html")
$dockCss  = [System.IO.File]::ReadAllText("$repo\src\shared\dock.css")
$dockJs   = [System.IO.File]::ReadAllText("$repo\src\shared\dock.js")
if ($dockHtml -match 'dock-contact|__CONTACT__|calendly\.com') { throw "build-library: a contact/calendly dock item resurfaced" }

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
