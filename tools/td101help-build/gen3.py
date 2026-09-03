# -*- coding: utf-8 -*-
# Deploy-ready hosted pages: external WebP images, lazy loading, real dimensions.
import os
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
ENROLL_HREF = "https://go.mucusfreelife.com/td101-jc-1"
ENROLL_TEXT = "CLICK HERE TO ENROLL"
ENROLL_SUB = "live.mucusfreelife.com/td101"
HELP_HREF = "https://live.mucusfreelife.com/helpdesk-1"
TITLE = "How To Get Into Transition Diet 101"
FOOT_1 = "Stuck on any step?"
FOOT_2 = "Our support team can get you in:"
FOOT_3 = "Use that link rather than replying to the email, so nothing gets missed."

NOAPP_SUB = "On your phone, no app needed. Scroll down and do one picture at a time."
APP_SUB = "On your phone, with the Circle app. Scroll down and do one picture at a time."

NOAPP_STEPS = [
    ("Fill in the form", ["Type your first name, last name and email.", "Pick your country code, then type your phone number.", "Tap the little square so it agrees to the terms.", "Tap the green ENROLL ME FREE button."], False),
    ("Go to your email", ["Two emails will arrive from us.", "You want the one about your invitation.", "Nothing there? Wait five minutes, then look in Spam or Promotions."], False),
    ("Open the invitation email", ["It says \"Prof. Spira has invited you to join\".", "Tap it to open it."], False),
    ("Tap Accept invitation", ["The blue button in the middle of the email.", "Your phone opens a web page. Carry on at step 7."], False),
    ("Only if a \"Log in\" screen appears", ["Most people go straight to step 7 and never see this.", "If you do see it, tap the blue Sign in with an email.", "Ignore the Google, Twitter and Facebook buttons."], True),
    ("Only if it asks for a password you do not have", ["You have not made a password yet, so there is nothing to type here.", "Tap the blue Sign up.", "That takes you to step 7."], True),
    ("Make your account", ["Type your full name.", "Make up a password and type it into both boxes.", "Write that password down somewhere. You will want it later.", "Tick the box, then tap the blue Accept invitation."], False),
    ("Create your profile", ["Type your full name in the box.", "A photo is not needed.", "Then scroll down the page."], False),
    ("Skip to the bottom", ["Website, Twitter, Facebook, Instagram, LinkedIn - leave them all empty.", "Tap the blue Continue button at the bottom."], False),
    ("You are in", ["A welcome box says hello by name.", "Tap the black Get started button."], False),
    ("Open the checklist", ["A short checklist slides up from the bottom.", "Tap the line that says Start the Transition Diet 101 Course."], False),
    ("Go to the course", ["The line opens up and shows a blue button.", "Tap Go to Transition Diet 101."], False),
    ("Start the course", ["This is the course. 42 lessons, all free.", "Tap the blue Start button."], False),
    ("The disclaimer page", ["One page to read before you begin.", "Tap the white Complete button at the bottom.", "That takes you straight into the first lesson."], False),
    ("Start watching", ["Press play on the video.", "When the lesson finishes, tap Complete at the bottom.", "That moves you to the next lesson. Do that every time."], False),
]

APP_STEPS = [
    ("Fill in the form", ["Type your first name, last name and email.", "Pick your country code, then type your phone number.", "Tap the little square so it agrees to the terms.", "Tap the green ENROLL ME FREE button."], False),
    ("Go to your email", ["Two emails will arrive from us.", "You want the one about your invitation.", "Nothing there? Wait five minutes, then look in Spam or Promotions."], False),
    ("Open the invitation email", ["It says \"Prof. Spira has invited you to join\".", "Tap it to open it."], False),
    ("Tap Accept invitation", ["The blue button in the middle of the email.", "Your phone will open the Circle app."], False),
    ("Type your email in the app", ["Use the same email you typed on the form in step 1.", "Tap Continue."], False),
    ("Leave the app for a second", ["The app is now waiting for a 6 number code.", "That code has just been emailed to you.", "Go back to your email again."], False),
    ("Open the email from Circle", ["It says \"Your temporary Circle login code\".", "Tap it to open it."], False),
    ("Read the 6 numbers", ["The big number in the email is your code.", "Remember it, or keep this email open."], False),
    ("Type the code into the app", ["Go back to the Circle app.", "Type the 6 numbers into the boxes.", "You do not press anything. It opens on its own."], False),
    ("Tap Complete profile", ["You are in. It welcomes you by name.", "Tap the white Complete profile button."], False),
    ("Type your name", ["Only the top box matters. That is your name.", "You can leave everything else empty."], False),
    ("Save it", ["The check mark is in the top right corner.", "Tap it once. That saves your profile."], False),
    ("Tap the blue link", ["Scroll down a little on the welcome post.", "Tap CLICK HERE TO ACCESS THE TRANSITION DIET 101.", "No link there? Tap the black Get started button instead, then tap Start the Transition Diet 101 Course."], False),
    ("The disclaimer page", ["One page to read before you start.", "Tap the white Complete button at the bottom."], False),
    ("Tap Continue", ["This is the course itself. 42 lessons.", "Tap the white Continue button at the bottom."], False),
    ("Start watching", ["Press play on the video.", "When the lesson finishes, tap Complete at the bottom.", "That moves you to the next lesson. Do that every time."], False),
]

CSS = """
  :root { --green:#14331F; --gold:#E3B84E; --cream:#F7F3E8; --ink:#23301D;
          --card:#FFFFFF; --line:#DCD5C2; --muted:#6B7263; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--cream); font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
         color:var(--ink); -webkit-text-size-adjust:100%; }
  .wrap { max-width:480px; margin:0 auto; padding:0 14px 90px; }
  .hero { background:var(--green); color:#fff; border-radius:0 0 18px 18px; padding:26px 20px 24px; text-align:center; }
  .hero .eyebrow { color:var(--gold); font-weight:700; letter-spacing:.14em; font-size:12px; text-transform:uppercase; margin:0 0 10px; }
  .hero h1 { margin:0 0 12px; font-size:26px; line-height:1.2; font-weight:800; }
  .hero p { margin:0 0 18px; font-size:17px; line-height:1.5; color:#EDE7D4; }
  .enroll { display:block; background:var(--gold); color:var(--green); text-decoration:none;
          border-radius:12px; padding:14px 16px 11px; font-weight:800; font-size:19px; }
  .enroll span { display:block; font-weight:600; font-size:13px; margin-top:2px; color:#3D5233; }
  .step { background:var(--card); border:1px solid var(--line); border-radius:14px; margin-top:22px; overflow:hidden; }
  .step header { background:var(--green); color:#fff; display:flex; align-items:center; gap:12px; padding:12px 14px; }
  .num { flex:0 0 40px; width:40px; height:40px; border-radius:50%; background:var(--gold); color:var(--green);
          font-weight:800; font-size:20px; display:flex; align-items:center; justify-content:center; }
  .step h2 { margin:0; font-size:18px; line-height:1.25; font-weight:800; text-transform:uppercase; letter-spacing:.02em; }
  .onlyif h2 { text-transform:none; }
  .onlyif .chip { display:inline-block; background:var(--gold); color:var(--green); font-size:11px; font-weight:800;
          letter-spacing:.1em; border-radius:6px; padding:2px 8px; margin-bottom:4px; }
  .step ul { margin:0; padding:14px 16px 14px 34px; }
  .step li { font-size:17px; line-height:1.55; margin-bottom:8px; }
  .step li:last-child { margin-bottom:0; }
  .step img { display:block; width:100%; height:auto; border-top:1px solid var(--line); }
  .foot { margin-top:30px; background:var(--green); color:#fff; border-radius:14px; padding:20px 18px; text-align:center; }
  .foot h3 { margin:0 0 8px; font-size:20px; }
  .foot p { margin:0 0 14px; font-size:16px; color:#EDE7D4; }
  .foot .small { margin:12px 0 0; font-size:13px; color:#C9CFBF; }
  .helpbtn { display:inline-block; background:#fff; color:var(--green); font-weight:800; text-decoration:none;
          border-radius:10px; padding:12px 22px; font-size:17px; }
  .stick { position:fixed; left:0; right:0; bottom:0; background:var(--cream); border-top:1px solid var(--line);
          padding:9px 14px; display:flex; align-items:center; justify-content:center; gap:10px; }
  .stick span { font-size:14px; color:var(--muted); }
  .stick a { font-size:14px; font-weight:800; color:var(--green); }
  a:focus-visible { outline:3px solid var(--gold); outline-offset:2px; }
"""

def build(folder, sub, steps, page_title):
    p = []
    p.append('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    p.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    p.append('<title>%s</title>' % page_title)
    p.append('<meta name="robots" content="noindex">')
    p.append('<style>%s</style></head><body>' % CSS)
    p.append('<div class="wrap">')
    p.append('<div class="hero"><p class="eyebrow">Transition Diet 101</p>'
             '<h1>%s</h1><p>%s</p>'
             '<a class="enroll" href="%s">%s<span>%s</span></a></div>'
             % (TITLE, sub, ENROLL_HREF, ENROLL_TEXT, ENROLL_SUB))
    for i, (title, bullets, onlyif) in enumerate(steps, 1):
        im = Image.open(os.path.join(D, 'deploy', folder, 'img', '%02d.webp' % i))
        w, h = im.size
        cls = "step onlyif" if onlyif else "step"
        head = ('<div><span class="chip">ONLY IF</span><h2>%s</h2></div>' % title) if onlyif else ('<h2>%s</h2>' % title)
        lis = "".join("<li>%s</li>" % b for b in bullets)
        lazy = '' if i == 1 else ' loading="lazy"'
        p.append('<section class="%s"><header><div class="num">%d</div>%s</header>'
                 '<ul>%s</ul><img src="img/%02d.webp" width="%d" height="%d" alt="Step %d screenshot" decoding="async"%s></section>'
                 % (cls, i, head, lis, i, w, h, i, lazy))
    p.append('<div class="foot"><h3>%s</h3><p>%s</p>'
             '<a class="helpbtn" href="%s">Get help here</a>'
             '<p class="small">%s</p></div>' % (FOOT_1, FOOT_2, HELP_HREF, FOOT_3))
    p.append('</div><div class="stick"><span>%s</span><a href="%s">Get help</a></div>' % (FOOT_1, HELP_HREF))
    p.append('</body></html>')
    out = os.path.join(D, 'deploy', folder, 'index.html')
    open(out, 'w', encoding='utf-8').write('\n'.join(p))
    print(folder, 'index.html', os.path.getsize(out) // 1024, 'KB')

build('noapp', NOAPP_SUB, NOAPP_STEPS, 'TD 101 - How To Get In (No App)')
build('circleapp', APP_SUB, APP_STEPS, 'TD 101 - How To Get In (Circle App)')
