# RETIRED 2026-10-26. Since 25 Oct 2026 jcj\ (jcsjournals.com) is the TD101 course page: tools\build-td101-page.py
# writes td101page\ and tools\build-all.ps1 copies it over jcj\. This script rebuilt jcj\ from the OLD hub master,
# so running it would silently replace the live course page with the old hub. It refuses to run. Remove the throw
# only if JC asks for the old hub back on jcsjournals.com.
throw "split-jcj.ps1 is retired: it would overwrite the live jcsjournals.com course page (jcj\) with the old hub"

# Splits the JC's Journals master (jcj-page.html) into the CDN-hosted
# jcj/{jcj.css, jcj.html, jcj.js} files of this repo. Same marker logic as
# split-library.ps1; drops the mockup-only bits (.mock-note CSS, the mock-note
# div, the hideNote JS binding).
$src  = "D:\00. MUCUS-FREE LIFE\01. Operations\02. Working Procedures\Claude SOPs\00. JC Brand\JC Website\site-masters\jcj-page.html"
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
  throw "Marker scan failed: style $styleStart..$styleEnd script $scriptStart..$scriptEnd"
}

$css = @(':root{color-scheme:dark}')
for ($i = $styleStart + 1; $i -lt $styleEnd; $i++) {
  if ($lines[$i] -match '^\.mock-note') { continue }
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

[System.IO.File]::WriteAllText("$repo\jcj\jcj.css",  (($css  -join "`n") + "`n"), $enc)
[System.IO.File]::WriteAllText("$repo\jcj\jcj.html", (($body -join "`n") + "`n"), $enc)
[System.IO.File]::WriteAllText("$repo\jcj\jcj.js",   (($js   -join "`n") + "`n"), $enc)
Write-Output ("css lines: "  + $css.Count)
Write-Output ("html lines: " + $body.Count)
Write-Output ("js lines: "   + $js.Count)
Write-Output "split-jcj OK"
