# -*- coding: utf-8 -*-
"""Export JC's desktop walkthrough Google Doc to HTML and split out its images.

SOURCE OF TRUTH, JC's own words 2026-09-03:
  "its the one with more photos the ine that has the disclaimer picture on it
   its the most recently freated one"
  => doc 17z2Ml9_d18W1nn8NxejKmcrCqU4FP_6-w09CrPQkVvY
     "TD 101 - How To Get In - COMPUTER (NO ACCOUNT) - with photos 10-12"

MEASURED 2026-09-03: that doc's TEXT is character-identical to Prof. Spira's
"edited 2026-09-01" copy (17jXggsEk0K3xtYl-4BZ7XSee0EOYWNq4W2eFVsAi5rI) apart
from blank-line placement, so there is no copy conflict to reconcile. It
carries 12 steps; JC's earlier 1A2GcNML... draft carried only 10 and had no
help footer.

⭐ NO CREDENTIALS NEEDED. The doc's sharing is role=reader / type=anyone
(MEASURED 2026-09-03), so the plain public export endpoint serves it. Do NOT
reintroduce a service-account path here: it needs a secret this build has no
business touching, and the public URL is one HTTP GET.

Writes into src/desktop-doc/ beside this script so the build never depends on
a temp scratchpad again.
"""
import base64
import os
import re
import sys
import urllib.request

DOC_ID = "17z2Ml9_d18W1nn8NxejKmcrCqU4FP_6-w09CrPQkVvY"
EXPORT = "https://docs.google.com/document/d/%s/export?format=html" % DOC_ID
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "src", "desktop-doc")


def export_html(dest):
    req = urllib.request.Request(EXPORT, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    if b"<img" not in data:
        raise SystemExit("export carried no images; the doc may have lost its "
                         "anyone-with-link sharing")
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)


def split_images(html_path, img_dir):
    os.makedirs(img_dir, exist_ok=True)
    html = open(html_path, encoding="utf-8", errors="replace").read()
    hits = re.findall(r'src="data:image/(png|jpeg|jpg);base64,([^"]+)"', html)
    paths = []
    for i, (kind, b64) in enumerate(hits, 1):
        ext = "png" if kind == "png" else "jpg"
        p = os.path.join(img_dir, "%02d.%s" % (i, ext))
        with open(p, "wb") as f:
            f.write(base64.b64decode(b64))
        paths.append(p)
    # strip the base64 payloads so the text skeleton stays readable and greppable
    skeleton = re.sub(r'src="data:image/(?:png|jpeg|jpg);base64,[^"]+"',
                      'src="IMG"', html)
    open(os.path.join(img_dir, "_skeleton.html"), "w",
         encoding="utf-8").write(skeleton)
    return paths


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    html_path = os.path.join(OUT, "desktop-doc.html")
    if "--reuse" in sys.argv and os.path.exists(html_path):
        print("reusing", html_path, os.path.getsize(html_path), "bytes")
    else:
        print("exported", html_path, export_html(html_path), "bytes")
    paths = split_images(html_path, OUT)
    print("images extracted:", len(paths))
    from PIL import Image
    for p in paths:
        im = Image.open(p)
        print(" ", os.path.basename(p), im.size, os.path.getsize(p), "bytes")
