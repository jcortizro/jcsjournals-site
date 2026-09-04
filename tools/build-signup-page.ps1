# Builds the WAITLIST / EMAIL CAPTURE page (td101.carrd.co).
#
# Same family shell as the other three sites: it is generated FROM the library
# master, so it inherits the shared header, footer, dock bar and background for
# free and can never drift from them. Only the main content is swapped, exactly
# the way the library page is generated from the landing shell.
#
# Input : site-masters\mdhs-library-page.html   (run build-library-page.ps1 first)
# Parts : src\signup\signup.{part.html,css,js}
# Output: site-masters\signup-page.html         (split-signup.ps1 makes the CDN files)
$ErrorActionPreference = 'Stop'
$repo    = "C:\Users\taino\jcsjournals-site"
$masters = "D:\00. MUCUS-FREE LIFE\01. Operations\02. Working Procedures\Claude SOPs\00. JC Brand\JC Website\site-masters"
. "$repo\tools\urls.ps1"
$utf8 = New-Object System.Text.UTF8Encoding($false)

$h = [IO.File]::ReadAllText("$masters\mdhs-library-page.html", [Text.Encoding]::UTF8)

# ---- swap the library's content for the signup content ----
# Stop BEFORE the dock bar: in this shell the footer and the dock live INSIDE
# <main>, so matching through </main> would swallow both. The master's closing
# </main> after the footer still closes the <main> this part opens.
$part = [IO.File]::ReadAllText("$repo\src\signup\signup.part.html", [Text.Encoding]::UTF8)
#
# The legal modal lives inside that swapped region, two lines above the dock.
# The shared footer this page inherits carries three [data-modal] buttons that
# open it, and the shared script binds it at top level, so dropping it both
# breaks the legal links and throws on load, killing the dock menus and the
# waitlist form. Carry it across, exactly as the siblings have it.
$rxModal = '(?s)<dialog id="legalModal".*?</dialog>'
$mm = [regex]::Matches($h, $rxModal)
if ($mm.Count -ne 1) { throw "build-signup: legal modal matched $($mm.Count), expected 1" }
$modal = $mm[0].Value

$rx = '(?s)<div class="bg-photo".*?(?=<nav class="dockbar")'
$m = [regex]::Matches($h, $rx)
if ($m.Count -ne 1) { throw "build-signup: content block matched $($m.Count), expected 1" }
$h = $h.Replace($m[0].Value, $part.TrimEnd() + "`n`n" + $modal + "`n`n")
Write-Output "  content swapped + legal modal kept : ok"

# ---- header: the wordmark goes HOME, this is not the hub ----
$n = ([regex]::Matches($h, '__HEADER__')).Count
if ($n -ne 1) { throw "build-signup: expected 1 header token, found $n" }
$hdr = [IO.File]::ReadAllText("$repo\src\jcj-parts\new-header.html", [Text.Encoding]::UTF8)
if (([regex]::Matches($hdr, [regex]::Escape('href="#top"'))).Count -ne 1) { throw "build-signup: header wordmark anchor not found once" }
$h = $h.Replace('__HEADER__', $hdr.Replace('href="#top"', 'href="' + $LandingUrl + '"'))

# ---- tokens ----
$h = $h.Replace('__RECIPESURL__', $RecipesUrl).Replace('__LIBRARYURL__', $LibraryUrl)

# ---- component css + js ----
$css = [IO.File]::ReadAllText("$repo\src\signup\signup.css", [Text.Encoding]::UTF8)
$js  = [IO.File]::ReadAllText("$repo\src\signup\signup.js",  [Text.Encoding]::UTF8)
$js  = $js.Replace('__FORMENDPOINT__', $FormEndpoint)

# Carrd flattens embed code to ONE line, so a line comment would kill the rest
# of the program. Gate it here, where it actually ships.
$flat = ($js -replace "`r`n", ' ') -replace "`n", ' '
$flat = [regex]::Replace($flat, '/\*.*?\*/', '')
$flat = $flat -replace 'https?://', ''
if ($flat.Contains('//')) { throw "build-signup: signup.js has a line comment, which Carrd's one-line flattening would fatal" }

$n = ([regex]::Matches($h, '</style>')).Count
if ($n -ne 1) { throw "build-signup: expected 1 </style>, found $n" }
$h = $h.Replace('</style>', ("/* ==== SIGNUP ==== */`n" + $css + "`n</style>"))

$n = ([regex]::Matches($h, '</script>')).Count
if ($n -ne 1) { throw "build-signup: expected 1 </script>, found $n" }
$h = $h.Replace('</script>', ("`n/* ==== SIGNUP ==== */`n" + $js + "`n</script>"))

# ---- title ----
$h = [regex]::Replace($h, '(?s)<title>.*?</title>', '<title>Transition Diet 101 &middot; Get Access</title>')

# ---- guards ----
foreach ($tok in @('__HEADER__', '__RECIPESURL__', '__LIBRARYURL__', '__FORMENDPOINT__')) {
  if ($h.Contains($tok)) { throw "build-signup: unresolved token $tok" }
}
if ([regex]::Matches($h, 'td101landing|td101library').Count -ne 0) { throw "build-signup: dead subdomain reference" }
if ([regex]::Matches($h, '<nav class="dockbar"').Count -ne 1) { throw "build-signup: expected exactly 1 inherited dock" }
if ([regex]::Matches($h, 'substack\.com/embed').Count -ne 1) { throw "build-signup: the Substack embed is missing" }
# The inherited footer's legal links are useless without the modal they open,
# and the shared script binds it at top level.
if ([regex]::Matches($h, 'id="legalModal"').Count -ne 1) { throw "build-signup: the legal modal is missing" }
if ([regex]::Matches($h, 'id="modalContent"').Count -ne 1) { throw "build-signup: the modal content slot is missing" }
if ([regex]::Matches($h, 'data-modal').Count -lt 3) { throw "build-signup: the footer legal links are missing" }

# ---- GATE: this page makes exactly ONE promise ----
# JC, 2026-08-11: "remove the promises that there's no spam, they only receive
# one email, because I'm not the one in charge of marketing... the main thing is
# that they'll get access to Transition Diet 101, they'll be notified the second
# it drops. That's the only promise."
# He does not control the mailing, so he cannot promise volume, frequency,
# unsubscribe behaviour or absence of spam. Anything that creeps back in is a
# claim he would have to keep, so the build refuses it. This checks the SHIPPED
# page, comments included, because a comment ships too.
#
# 2026-09-03, D174-CLASS FIX. This list used to be BARE SUBSTRINGS compared with
# ToLower().Contains(): 'no spam', 'unsubscribe', 'one email', 'nothing else'.
# That tests the WORDS; the law is about the CLAIM. JC dictated copy the same day
# telling the reader to "check your spam, junk, or promotions folder", which is
# an INSTRUCTION about where to look, not a promise that he will not send spam.
# A word-level pattern eventually eats legitimate copy exactly the way the 9/02
# Contact guard false-fired on the library's own "get in contact" body text.
# Every pattern below must now match the PROMISE, and carries the reason it is
# banned so a later session cannot mistake it for a style preference.
$bannedClaims = @(
  @{ rx = '(?i)\b(no|zero|never\s+any)\s+spam\b';
     why = 'promises there will be no spam' },
  @{ rx = '(?i)\b(never|not|won.?t|will\s+not|do\s+not|don.?t)\s+spam\b';
     why = 'promises not to spam' },
  @{ rx = '(?i)\bspam[\s-]?free\b';
     why = 'promises spam-free mail' },
  @{ rx = '(?i)\bunsubscribe\b';
     why = 'describes unsubscribe behaviour, which Substack controls and he does not' },
  @{ rx = '(?i)\b(only\s+|just\s+)?(one|1|two|a\s+single)\s+emails?\b';
     why = 'promises how many emails arrive' },
  @{ rx = '(?i)(\bnothing\s+else\b[^.<]{0,40}\b(email|inbox|list|send|sent)\b|\b(email|inbox|list|send|sent)\b[^.<]{0,40}\bnothing\s+else\b)';
     why = 'promises nothing else will be sent' }
)
foreach ($claim in $bannedClaims) {
  $hit = [regex]::Matches($h, $claim.rx)
  if ($hit.Count -gt 0) {
    throw ("build-signup: the page " + $claim.why + " (matched '" + $hit[0].Value + "'). " +
           "JC does not run the mailing, so email volume, frequency, unsubscribe behaviour " +
           "and absence of spam are not his to promise. Telling a reader WHERE TO LOOK is " +
           "fine; promising how the mail behaves is not.")
  }
}
# 2026-09-02, JC's dictation: the course is OPEN, so the one promise changed
# from "notified the second it drops" to "the email gives you access". Match the
# invariant phrase, not one exact sentence, so JC can reword around it without
# the gate firing on his own copy. The promise itself still cannot go missing.
# 2026-09-03, RE-BASELINED DELIBERATELY. He dictated the promise copy word for
# word and 'gives you access' is not in it any more. The promise was FOUR
# facts and each one was checked, because he named all four: the email is
# automatic, its subject line is "Transition Diet 101 Access Guide", it explains
# how to make the account, and it says where to look if it does not show up.
# 2026-09-03, RE-BASELINED AGAIN, LATER THE SAME DAY, on JC's direct
# instruction. The hint paragraph under the embed was deleted and replaced by a
# shorter line ABOVE the embed, which carries TWO of those four facts. He was
# told in advance that this gate would break and that the other two facts would
# leave the site, and he answered "no you are supposed to change the site".
# So the gate now enforces only what his copy actually claims. A gate that
# outlives its copy fires on his own writing and teaches him to ignore it.
# The sentences around them stay his to reword without tripping this gate.
# EACH SURVIVING PATTERN BELOW WAS PROVEN TO FAIL by deleting its fact and
# rebuilding, re-proven after this re-baseline.
# 2026-09-03, THIRD RE-BASELINE, same day, on JC's instruction "i went with
# system b". He changed the Substack welcome email's SUBJECT from
# "Transition Diet 101 Access Guide" to
# "One step left: create your Transition Diet 101 account", so the page had to
# follow it or the instruction to search a spam folder would point at a string
# that no longer exists. THE SUBJECT HERE MUST EQUAL THE LIVE SUBSTACK SUBJECT.
# If you change one, change the other in the same commit. The live subject is
# at Substack > Settings > Emails > Welcome email to new subscribers.
# Case-insensitive on purpose: capitalization is presentation and is his to
# change, the words are the fact and are not.
$promiseInvariants = @(
  @{ rx = '(?i)One step left: create your Transition Diet 101 account';
     what = 'the subject line of the access email, which must match Substack' },
  # Removed 2026-09-03 on JC's direct instruction: the hint paragraph was
  # replaced with a shorter line above the embed that does not carry this fact.
  # It was:  rx   = '(?i)automatic[\s\S]{0,160}?Transition Diet 101 Access Guide'
  #          what = 'that THAT email is the one sent automatically'
  # WARNING, kept for whoever restores it: a bare '\bautomatic' CANNOT fail,
  # because the inherited library body already contains the word, so the check
  # passes with the promise deleted. That is why it was a PROXIMITY match to
  # the subject line and not a lone word.
  # Removed 2026-09-03 on JC's direct instruction: the hint paragraph was
  # replaced with a shorter line above the embed that does not carry this fact.
  # It was:  rx   = '(?i)create your account'
  #          what = 'that the email explains how to create the account'
  @{ rx = '(?i)\b(spam|junk|promotions)\b[^<]{0,40}folder';
     what = 'where to look if the email does not show up' }
)
foreach ($inv in $promiseInvariants) {
  if ([regex]::Matches($h, $inv.rx).Count -lt 1) {
    throw ("build-signup: the one promise is broken, the page no longer states " + $inv.what)
  }
}
Write-Output "  one promise only, no email claims : ok"
# Every element the component toggles with .hidden needs an explicit
# [hidden]{display:none}, because an author display rule outranks the browser's.
# Without it a successful signup renders the filled form and a stuck "Sending..."
# button underneath the success panel, while the script still reads hidden=true.
foreach ($sel in @('#waitform\[hidden\]', '\.signdone\[hidden\]')) {
  if ([regex]::Matches($h, $sel).Count -lt 1) {
    throw "build-signup: missing a [hidden] display rule for $sel, so JS cannot hide it"
  }
}
if ([regex]::Matches($h, 'class="acc cat"').Count -ne 0) { throw "build-signup: library topics leaked into the signup page" }

[IO.File]::WriteAllText("$masters\signup-page.html", $h, $utf8)
Write-Output ("signup page written: " + [math]::Round((Get-Item "$masters\signup-page.html").Length / 1kb) + " KB")
