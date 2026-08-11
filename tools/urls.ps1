# THE ONLY PLACE THE SITE'S PAGE URLS ARE DEFINED.
# When JC moves the landing page to jcsjournals.com (or moves the library),
# change the value(s) here, then run tools\build-all.ps1 and push. Done.
# Trailing slash required.
# 2026-08-10: JC renamed the Carrd sites. The old td101landing subdomain is
# dead and the hub is jcsjournals.com, so "landing" now routes to the hub.
$LandingUrl = "https://jcsjournals.com/"
$LibraryUrl = "https://freelibrary.carrd.co/"
# The recipe book's own site (used by the library dropdown + the dock bar).
$RecipesUrl = "https://freerecipes.carrd.co/"
# The Transition Diet 101 waitlist / email capture page (JC 2026-08-11).
$SignupUrl  = "https://td101.carrd.co/"
# The Google Apps Script web app that receives the waitlist form and appends a
# row to JC's sheet. EMPTY until he deploys it: the form then tells people the
# waitlist is not connected yet rather than silently dropping their details.
$FormEndpoint = ""
