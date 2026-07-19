# Assembles the LANDING page master from src\home.part.html + src assets.
# src\home.part.html is the EDITABLE SOURCE for the landing page (and for the
# library's shell, via build-library-page.ps1). Never hand-edit the outputs.
$repo = "C:\Users\taino\jcsjournals-site"
$masters = "D:\00. MUCUS-FREE LIFE\01. Operations\02. Working Procedures\Claude SOPs\00. JC Brand\JC Website\site-masters"
. "$repo\tools\urls.ps1"
$enc = New-Object System.Text.UTF8Encoding($false)

$part = [System.IO.File]::ReadAllText("$repo\src\home.part.html")
$assets = [System.IO.File]::ReadAllText("$repo\src\montserrat.css") + "`n" + [System.IO.File]::ReadAllText("$repo\src\source-sans-3.css")
$bg64 = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes("$repo\src\foliage.jpg"))

$page = $part.Replace('/*__ASSETS__*/', $assets).Replace('__BGIMG__', $bg64).Replace('__LIBURL__', $LibraryUrl)
if ($page.Contains('__LIBURL__') -or $page.Contains('__BGIMG__') -or $page.Contains('__ASSETS__')) { throw "unresolved tokens remain" }

[System.IO.File]::WriteAllText("$masters\mfl-home-redesign-v1.html", $page, $enc)
Write-Output ("landing page built: " + (Get-Item "$masters\mfl-home-redesign-v1.html").Length + " bytes")
