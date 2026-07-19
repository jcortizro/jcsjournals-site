# Splits the MFL home master (mfl-home-v1.html) into CDN-hosted
# home/{home.css, home.html, home.js}. Marker-based. Drops the mockup-only
# mock-note div, its CSS rules, and the hideNote JS binding (leaving the
# binding in with no div would throw and kill the rest of the JS).
$src  = "D:\00. MUCUS-FREE LIFE\01. Operations\02. Working Procedures\Claude SOPs\00. JC Brand\JC Website\site-masters\mfl-home-v1.html"
$repo = "C:\Users\taino\jcsjournals-site"
New-Item -ItemType Directory -Force "$repo\home" | Out-Null
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
  throw "Marker scan failed: style $styleStart..$styleEnd script $scriptStart..$scriptEnd"
}

$css = @()
$inMock = $false
for ($i = $styleStart + 1; $i -lt $styleEnd; $i++) {
  if ($lines[$i] -match '^\.mock-note') { continue }
  if ($lines[$i] -match '^/\* ---- mock note ---- \*/$') { continue }
  # the mobile media block references .mock-note{bottom:78px}; harmless if kept, strip just that rule line
  if ($lines[$i].Trim() -eq '.mock-note{bottom:78px}') { continue }
  $css += $lines[$i]
}

$body = @()
for ($i = $styleEnd + 1; $i -lt $scriptStart; $i++) {
  if ($lines[$i] -match 'class="mock-note"') { continue }
  $body += $lines[$i]
}
while ($body.Count -gt 0 -and $body[0].Trim() -eq '')  { $body = $body[1..($body.Count-1)] }
while ($body.Count -gt 0 -and $body[-1].Trim() -eq '') { $body = $body[0..($body.Count-2)] }

$js = @()
for ($i = $scriptStart + 1; $i -lt $scriptEnd; $i++) {
  if ($lines[$i] -match 'hideNote') { continue }
  $js += $lines[$i]
}

[System.IO.File]::WriteAllText("$repo\home\home.css",  (($css  -join "`n") + "`n"), $enc)
[System.IO.File]::WriteAllText("$repo\home\home.html", (($body -join "`n") + "`n"), $enc)
[System.IO.File]::WriteAllText("$repo\home\home.js",   (($js   -join "`n") + "`n"), $enc)
Write-Output ("css lines: "  + $css.Count)
Write-Output ("html lines: " + $body.Count)
Write-Output ("js lines: "   + $js.Count)
Write-Output "split OK"
