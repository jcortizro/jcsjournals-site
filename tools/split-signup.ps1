# Splits the signup master into signup/{signup.css, signup.html, signup.js},
# the three files the Carrd loader on td101.carrd.co fetches. Same marker logic
# as split-jcj.ps1.
#
# Drops the mockup-only hideNote JS binding, exactly as split-library.ps1 and
# split-jcj.ps1 do: the mock-note div does not exist here, so the binding throws
# at top level and kills every script after it, including the dock bar menus and
# the waitlist form handler itself. Nothing about that is visible in a
# screenshot, which is why the gate at the bottom of this file exists.
$src  = "D:\00. MUCUS-FREE LIFE\01. Operations\02. Working Procedures\Claude SOPs\00. JC Brand\JC Website\site-masters\signup-page.html"
$repo = "C:\Users\taino\jcsjournals-site"
$lines = [System.IO.File]::ReadAllLines($src)
$enc = New-Object System.Text.UTF8Encoding($false)

$styleStart = -1; $styleEnd = -1; $scriptStart = -1; $scriptEnd = -1
for ($i = 0; $i -lt $lines.Length; $i++) {
  $l = $lines[$i].Trim()
  if ($l -eq '<style>'   -and $styleStart  -lt 0) { $styleStart  = $i }
  elseif ($l -eq '</style>'  -and $styleEnd    -lt 0) { $styleEnd    = $i }
  elseif ($l -eq '<script>'  -and $scriptStart -lt 0) { $scriptStart = $i }
  elseif ($l -eq '</script>') { $scriptEnd = $i }
}
if ($styleStart -lt 0 -or $styleEnd -lt 0 -or $scriptStart -lt 0 -or $scriptEnd -lt 0) {
  throw "split-signup: marker scan failed: style $styleStart..$styleEnd script $scriptStart..$scriptEnd"
}

$css = @(':root{color-scheme:dark}')
for ($i = $styleStart + 1; $i -lt $styleEnd; $i++) { $css += $lines[$i] }

$body = @()
for ($i = $styleEnd + 1; $i -lt $scriptStart; $i++) { $body += $lines[$i] }
while ($body.Count -gt 0 -and $body[0].Trim() -eq '')  { $body = $body[1..($body.Count-1)] }
while ($body.Count -gt 0 -and $body[-1].Trim() -eq '') { $body = $body[0..($body.Count-2)] }

$js = @()
for ($i = $scriptStart + 1; $i -lt $scriptEnd; $i++) {
  if ($lines[$i] -match 'hideNote') { continue }
  $js += $lines[$i]
}

New-Item -ItemType Directory -Force -Path "$repo\signup" | Out-Null
[System.IO.File]::WriteAllText("$repo\signup\signup.css",  (($css  -join "`n") + "`n"), $enc)
[System.IO.File]::WriteAllText("$repo\signup\signup.html", (($body -join "`n") + "`n"), $enc)
[System.IO.File]::WriteAllText("$repo\signup\signup.js",   (($js   -join "`n") + "`n"), $enc)
# ---- GATE: no top-level lookup of an element this page does not have ----
# In this flat generated file a statement at column 0 runs the moment the page
# loads, so any getElementById there must resolve or the whole script dies and
# takes the dock bar menus and the waitlist form with it. Two shapes have
# already shipped broken: a direct deref (hideNote) and a const binding used one
# line later (legalModal). So the gate reads EVERY id looked up by a top-level
# statement, whatever the syntax. Lines inside a function body are indented or
# start with "function", and are fine: this page simply never calls them.
$bodyText = ($body -join "`n")
$orphans = @()
foreach ($l in $js) {
  if ($l -match '^\s') { continue }
  if ($l -match '^function\b') { continue }
  foreach ($m in [regex]::Matches($l, "document\.getElementById\((['""])([A-Za-z0-9_\-]+)\1\)")) {
    $id = $m.Groups[2].Value
    if (-not [regex]::IsMatch($bodyText, 'id="' + [regex]::Escape($id) + '"')) { $orphans += $id }
  }
}
$orphans = $orphans | Select-Object -Unique
if ($orphans.Count -gt 0) {
  throw ("split-signup: top-level binding to absent element(s): " + ($orphans -join ', ') +
         ". That throws on load and kills the dock bar and the form.")
}
Write-Output "  no orphan top-level bindings : ok"

Write-Output ("css lines: "  + $css.Count)
Write-Output ("html lines: " + $body.Count)
Write-Output ("js lines: "   + $js.Count)
Write-Output "split-signup OK"
