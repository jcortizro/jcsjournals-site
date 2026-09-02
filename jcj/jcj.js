document.querySelectorAll('.more-btn').forEach(function(b){
  b.addEventListener('click',function(){
    var x=document.getElementById(b.dataset.more);
    var open=x.classList.toggle('open');
    b.textContent=open?'show less':b.dataset.label;
  });
  b.dataset.label=b.textContent;
});

/* ==== LIBRARY engine ==== */
document.addEventListener('click',e=>{const t=e.target.closest('.acc-trigger');if(t){const acc=t.parentElement;const open=acc.classList.toggle('open');t.setAttribute('aria-expanded',open);if(acc.classList.contains('cat')&&open){document.querySelectorAll('.acc.cat.open').forEach(c=>{if(c!==acc)closeCat(c);});setTimeout(()=>{const y=acc.getBoundingClientRect().top+window.scrollY-70;(function(){var de=document.documentElement,p=de.style.scrollBehavior;de.style.scrollBehavior='auto';window.scrollTo(0,y);de.style.scrollBehavior=p;})();},380);}}});




function openChain(id){let el=document.getElementById(id);if(!el)return;let node=el,topcat=null;while(node){if(node.classList&&node.classList.contains('acc')){node.classList.add('open');const tr=node.querySelector(':scope>.acc-trigger');if(tr)tr.setAttribute('aria-expanded','true');if(node.classList.contains('cat'))topcat=node;}node=node.parentElement;}if(topcat)document.querySelectorAll('.acc.cat.open').forEach(c=>{if(c!==topcat)closeCat(c);});setTimeout(()=>{const y=el.getBoundingClientRect().top+window.scrollY-70;(function(){var de=document.documentElement,p=de.style.scrollBehavior;de.style.scrollBehavior='auto';window.scrollTo(0,y);de.style.scrollBehavior=p;})();},380);}
document.querySelectorAll('[data-open]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();openChain(a.dataset.open);}));
document.querySelectorAll('[data-close-dd]').forEach(a=>a.addEventListener('click',()=>document.querySelectorAll('.dropdown').forEach(x=>x.classList.remove('open'))));
if(location.hash){const id=location.hash.slice(1);if(document.getElementById(id))openChain(id);}
const modal=document.getElementById('legalModal'),mc=document.getElementById('modalContent');
const LEGAL={terms:`
<h2>Terms of Use</h2><p class="eff">Effective Date: 9/2/2026 &middot; supersedes all prior versions</p>
<p>Welcome to this website (jcsjournals.com). By accessing or using this Site, you agree to the following Terms of Use. If you do not agree, please do not use the Site.</p>
<h3>Introduction</h3>
<p>By accessing or using this website (jcsjournals.com), you agree to the following Terms of Use. If you do not agree with these Terms, you must not use this Site. This Site is independently operated and is not the official website of Mucus-Free Life LLC and/or Eden Ministries Trust.</p>
<h3>What This Site Is</h3>
<p>This Site is an educational landing page. Its purpose is to expose visitors to information: perspectives on health, the Mucusless Diet Healing System (MDHS), and the teachings of Prof. Arnold Ehret, and to point visitors toward further reading, including the owner&rsquo;s newsletter on Substack. The Site presents these ideas so you can learn about them. It does not advocate, urge, or prescribe that any visitor adopt any practice described here.</p>
<h3>Educational Purpose Only</h3>
<p>The content on this Site, including videos, written material, and links, is provided strictly for informational and educational purposes. It is not medical advice, medical diagnosis, treatment, or a substitute for consultation with a licensed healthcare professional. Nothing on this Site creates a doctor-patient relationship or healthcare provider relationship. If you choose to apply any information presented here, you do so voluntarily and at your own discretion.</p>
<h3>Assumption of Risk</h3>
<p>By using this Site, you acknowledge that dietary and lifestyle changes involve inherent risks. You assume full responsibility for any actions you take based on the information presented on this Site. The owner of this Site is not responsible for any outcomes resulting from your personal decisions.</p>
<h3>No Commerce, No Accounts, No Data</h3>
<p>This Site:</p>
<ul><li>Does not sell products or services and does not collect payments.</li><li>Does not offer or manage user accounts or memberships.</li><li>Does not itself collect, store, or process personal information. There are no forms handled by this Site.</li><li>Contains no paid advertising and no affiliate links. The owner earns nothing from your use of this Site or from the links on it.</li></ul>
<h3>The Newsletter (Substack)</h3>
<p>This Site links to, and in places embeds, the sign-up box for the owner&rsquo;s newsletter, which is hosted and delivered by Substack (jcortizroman.substack.com). Subscribing happens entirely on Substack&rsquo;s platform: anything you enter into that box is sent to and processed by Substack, not by this Site. Your subscription is governed by Substack&rsquo;s own terms of service and privacy policy, and Substack provides its own tools for managing or ending a subscription.</p>
<h3>Affiliation Disclosure</h3>
<p>The owner of this Site is affiliated with Mucus-Free Life and appears in its educational materials, including the Transition Diet 101 course. However:</p>
<ul><li>This Site does not control or operate Mucus-Free Life platforms.</li><li>All courses, memberships, email lists, products, and services referenced through external links are independently operated by Mucus-Free Life LLC and/or Eden Ministries Trust and are governed by their own terms and policies.</li></ul>
<h3>External Links and Embedded Content</h3>
<p>This Site links to third-party platforms, including the owner&rsquo;s profiles on YouTube, Facebook, Instagram, and TikTok, the owner&rsquo;s Substack newsletter, companion pages operated by the owner (the free library, the free recipe book, and the Transition Diet 101 waitlist page), and educational platforms operated by Mucus-Free Life. Some third-party content, such as a video player or a newsletter sign-up box, is embedded directly in the page. The owner of this Site is not responsible for the content, policies, practices, or transactions of any external website or embedded service. Visiting those platforms or interacting with embedded content is done at your own discretion and under those platforms&rsquo; own terms.</p>
<h3>Intellectual Property</h3>
<p>Unless otherwise stated, all original content on this Site &mdash; including videos, written material, design elements, and branding &mdash; is the intellectual property of the Site owner. You may view the content for personal use only. You must not:</p>
<ul><li>Republish content from this Site</li><li>Reproduce or redistribute the video or written material</li><li>Use the content for commercial purposes</li><li>Modify or edit the content</li><li>Present the content as your own</li></ul>
<p>Unauthorized use is prohibited.</p>
<h3>Acceptable Use</h3>
<p>You must not use this Site in any way that:</p>
<ul><li>Causes damage to the Site</li><li>Interferes with its availability</li><li>Is unlawful, fraudulent, or harmful</li><li>Attempts automated data collection (scraping, mining, harvesting)</li><li>Transmits malicious software</li></ul>
<h3>No Warranties</h3>
<p>This Site is provided &ldquo;as is&rdquo; without warranties of any kind, express or implied. The owner makes no representations regarding the accuracy, completeness, or reliability of the information provided.</p>
<h3>Limitation of Liability</h3>
<p>To the fullest extent permitted by law, the owner of this Site shall not be liable for any direct, indirect, incidental, consequential, special, or business-related losses arising from the use of this Site, reliance on its content, or your interactions with any linked or embedded third-party platform. These limitations apply even if the possibility of such damages has been advised. Nothing in these Terms excludes liability where it would be unlawful to do so.</p>
<h3>Indemnification</h3>
<p>You agree to indemnify and hold harmless the owner of this Site from any claims, liabilities, damages, losses, or expenses arising from your use of the Site or violation of these Terms.</p>
<h3>Severability</h3>
<p>If any provision of these Terms is found unenforceable under applicable law, the remaining provisions will remain in effect.</p>
<h3>Governing Law</h3>
<p>These Terms shall be governed by and construed in accordance with the laws of the State of Washington, United States. Any disputes relating to these Terms shall be subject to the jurisdiction of the courts located within the United States.</p>
<h3>Changes to These Terms</h3>
<p>These Terms may be updated from time to time. Continued use of the Site after updates constitutes acceptance of the revised Terms.</p>
<h3>Contact</h3>
<p>For questions regarding these Terms, please contact: <a href="mailto:jcsjournals@gmail.com">jcsjournals@gmail.com</a></p>
`,medical:`
<h2>Medical Disclaimer</h2><p class="eff">Effective Date: 9/2/2026 &middot; supersedes all prior versions</p>
<p>Welcome to this website (jcsjournals.com). This Medical Disclaimer applies to all content on this Site.</p>
<h3>1. Educational Purpose Only</h3>
<p>The content shared on this platform is for educational and informational purposes only. This includes:</p>
<ul><li>Articles and written material</li><li>Videos and visual content</li><li>Menu examples</li><li>Explanations of the Mucusless Diet Healing System (MDHS)</li></ul>
<p>All material reflects:</p>
<ul><li>Personal study</li><li>Interpretation of existing teachings</li><li>Educational exploration</li></ul>
<p>This content is not intended as medical advice.</p>
<h3>2. Exposure, Not Advocacy</h3>
<p>This platform exists to expose you to a body of information and a historical dietary paradigm so that you can learn about it. It does not advocate, recommend, urge, or prescribe that you, or any specific person, adopt any practice described here. Whether to explore any of these ideas further is entirely your own decision, made at your own discretion and, where appropriate, with professional guidance.</p>
<h3>3. Not Medical Advice</h3>
<p>Nothing on this platform should be interpreted as:</p>
<ul><li>Medical advice</li><li>Diagnosis</li><li>Treatment recommendation</li><li>Health prescription</li></ul>
<p>I am not a licensed medical professional, physician, dietitian, or nutritionist. I share as a student documenting my learning and understanding of concepts originally developed by Arnold Ehret and interpreted through modern application. Always consult a qualified healthcare professional before making decisions related to your health.</p>
<h3>4. No Doctor&ndash;Patient Relationship</h3>
<p>Using this website, consuming content, subscribing to the newsletter, or interacting with any materials does not create a doctor&ndash;patient relationship or any professional-client relationship. No individualized guidance is being provided.</p>
<h3>5. Health &amp; Wellness Information</h3>
<p>This platform discusses topics including:</p>
<ul><li>Diet and food selection</li><li>Fasting and juice consumption</li><li>Elimination processes</li><li>Natural lifestyle practices</li></ul>
<p>These topics are presented within a historical and educational framework. No statements made on this platform are intended to:</p>
<ul><li>Diagnose conditions</li><li>Treat illness</li><li>Cure disease</li><li>Prevent medical issues</li></ul>
<p>Statements on this platform have not been evaluated by the Food and Drug Administration or any other health authority.</p>
<h3>6. Personal Responsibility</h3>
<p>By using this platform, you acknowledge and agree that:</p>
<ul><li>You are responsible for your own health decisions</li><li>You apply any information at your own discretion</li><li>You understand that results vary between individuals</li></ul>
<p>You assume full responsibility for any actions taken based on the information provided.</p>
<h3>7. No Guarantees</h3>
<p>No guarantees are made regarding:</p>
<ul><li>Results</li><li>Outcomes</li><li>Health improvements</li></ul>
<p>Any examples shared (including menus, experiences, or observations) are:</p>
<ul><li>Illustrative</li><li>Educational</li><li>Not predictive of your experience</li></ul>
<h3>8. Sensitive Practices and At-Risk Groups</h3>
<p>Some content may reference practices such as:</p>
<ul><li>Fasting</li><li>Dietary transitions</li><li>Elimination-related practices</li></ul>
<p>These can affect individuals differently, and this platform does not recommend that any specific person engage in them. Consult an appropriate licensed professional before beginning any dietary, weight loss, or exercise change, especially if you are pregnant or nursing, are under 18, take prescription medication, are managing a diagnosed condition, or have a history of disordered eating.</p>
<h3>9. External Resources</h3>
<p>This platform may reference or link to external materials, including books, courses, membership platforms, the owner&rsquo;s newsletter on Substack, and other third-party websites. These are shared for educational purposes. I do not control and am not responsible for their claims, their recommendations, or their outcomes.</p>
<h3>10. Emergency Notice</h3>
<p>If you are experiencing a medical emergency: call your local emergency number or seek immediate help from a licensed medical professional or emergency room. Do not rely on information from this platform.</p>
`,privacy:`
<h2>Privacy Policy</h2><p class="eff">Effective Date: 9/2/2026 &middot; supersedes all prior versions</p>
<p>Welcome to this website (jcsjournals.com). This Privacy Policy explains what information is, and is not, collected when you use this Site. The short version: this Site itself collects nothing.</p>
<h3>1. Overview</h3>
<p>This website is an educational landing page. It exists to share information related to the Mucusless Diet Healing System (MDHS) and to point visitors toward further reading, including the owner&rsquo;s newsletter on Substack. It is built to be read, not to gather data.</p>
<h3>2. What This Site Does Not Do</h3>
<p>This Site does not:</p>
<ul><li>Require or offer account creation</li><li>Operate any forms of its own &mdash; no data you type is sent to or stored by this Site</li><li>Collect names, email addresses, or contact information</li><li>Process payments</li><li>Run owner-operated analytics or tracking</li><li>Sell, rent, or share personal data &mdash; the owner has no such data to sell or share</li></ul>
<p>You can read everything on this Site without submitting any personal information.</p>
<h3>3. Hosting and Technical Logs</h3>
<p>This Site is served through third-party hosting infrastructure (Carrd and GitHub). Like virtually all web hosting, those providers may automatically log standard technical data such as IP address, browser type, device type, and pages requested, under their own privacy policies. The owner of this Site does not use any such logs to identify visitors.</p>
<h3>4. The Newsletter Sign-Up (Substack)</h3>
<p>Pages on this Site link to, and in places embed, the sign-up box for the owner&rsquo;s newsletter, which is hosted and delivered by Substack (jcortizroman.substack.com). That box is Substack&rsquo;s own embedded form. Anything you enter into it is transmitted directly to Substack, not to this Site. If you subscribe, your email address becomes part of the newsletter&rsquo;s subscriber list, which is stored and managed on Substack&rsquo;s platform and governed by Substack&rsquo;s privacy policy and terms. Substack provides its own tools for managing or ending a subscription at any time.</p>
<h3>5. Embedded Content and External Links</h3>
<p>This Site embeds some third-party content, such as a YouTube video player and the Substack sign-up box, and links to external platforms, including the owner&rsquo;s social media profiles (YouTube, Facebook, Instagram, TikTok), companion pages operated by the owner, and educational platforms operated by Mucus-Free Life. Embedded services and external platforms may collect usage data and set cookies of their own when you view or interact with them. They operate independently under their own privacy policies, and the owner of this Site is not responsible for how they collect, use, or store your data.</p>
<h3>6. Cookies</h3>
<p>The owner of this Site does not set cookies and does not use cookies for tracking. The hosting platform and embedded third-party services described above may set their own cookies under their own policies. You can block or clear cookies at any time through your browser settings.</p>
<h3>7. Your Choices</h3>
<p>You can choose to:</p>
<ul><li>Read this Site without entering any information anywhere</li><li>Avoid clicking external links or interacting with embedded content</li><li>Block or clear cookies through your browser settings</li></ul>
<h3>8. Changes to This Policy</h3>
<p>This Privacy Policy may be updated at any time. Continued use of the Site means you accept the latest version.</p>
<h3>9. Contact</h3>
<p>For questions about this Policy, please contact: <a href="mailto:jcsjournals@gmail.com">jcsjournals@gmail.com</a></p>
`};
document.querySelectorAll('[data-modal]').forEach(b=>b.addEventListener('click',()=>{mc.innerHTML=LEGAL[b.dataset.modal];modal.showModal();}));
modal.addEventListener('click',e=>{if(e.target===modal||e.target.closest('[data-close]'))modal.close();});

/* ---- next-topic rows + sticky wayfinder (2026-07-17) ---- */
function closeCat(c){c.classList.remove('open');const t=c.querySelector(':scope>.acc-trigger');if(t)t.setAttribute('aria-expanded','false');}
const CATS=[...document.querySelectorAll('.acc.cat')];
const NUM={};CATS.forEach((c,i)=>NUM[c.id]=i+1);
const NEXT={foundation:'menus',menus:'mechanics',mechanics:'enemas',enemas:'addiction',addiction:'faq',faq:null};
const SHORT={foundation:'What Is the MDHS?',menus:'Learn What to Eat',mechanics:'Learn How to Eat',enemas:'Waste Eliminator',addiction:'Addiction & Relapse',faq:'FAQ'};
function goLibrary(cat){if(cat)closeCat(cat);setTimeout(()=>{const y=document.getElementById('library').getBoundingClientRect().top+window.scrollY-60;(function(){var de=document.documentElement,p=de.style.scrollBehavior;de.style.scrollBehavior='auto';window.scrollTo(0,y);de.style.scrollBehavior=p;})();},380);}
CATS.forEach(cat=>{const row=document.createElement('div');row.className='nextrow';
const back=document.createElement('button');back.className='nbtn';back.innerHTML='<span class="triup" aria-hidden="true"></span>All topics';back.addEventListener('click',()=>goLibrary(cat));row.appendChild(back);
const n=NEXT[cat.id];const go=document.createElement('button');go.className='nbtn primary';
if(n){go.innerHTML='Next: <b>'+NUM[n]+'</b> '+SHORT[n]+' <span class="tri" aria-hidden="true"></span>';go.addEventListener('click',()=>openChain(n));}
else{go.innerHTML='See my social media <span class="tri" aria-hidden="true"></span>';go.addEventListener('click',()=>{closeCat(cat);setTimeout(()=>{window.location.href='#socials';},380);});}
row.appendChild(go);cat.appendChild(row);});
const wf=document.createElement('div');wf.className='wayfind';
wf.innerHTML='<button class="wf-top"><span class="triup" aria-hidden="true"></span>Topics</button><span class="wf-lbl"></span><button class="wf-next"></button>';
document.body.appendChild(wf);
const wfL=wf.querySelector('.wf-lbl'),wfN=wf.querySelector('.wf-next'),wfT=wf.querySelector('.wf-top');
let wfCat=null;
wfT.addEventListener('click',()=>goLibrary(wfCat));
wfN.addEventListener('click',()=>{if(!wfCat)return;const n=NEXT[wfCat.id];if(n)openChain(n);else{closeCat(wfCat);setTimeout(()=>{window.location.href='#socials';},380);}});
function wfUpdate(){let cur=null;for(const c of CATS){if(!c.classList.contains('open'))continue;const r=c.getBoundingClientRect();if(r.top<-40&&r.bottom>innerHeight*.55){cur=c;break;}}
if(cur){wfCat=cur;wfL.innerHTML='<b>'+NUM[cur.id]+'</b>'+SHORT[cur.id];wfN.innerHTML=(NEXT[cur.id]?'Next':'Done')+' <span class="tri" aria-hidden="true"></span>';wf.classList.add('show');}
else{wf.classList.remove('show');wfCat=null;}}
addEventListener('scroll',wfUpdate,{passive:true});addEventListener('resize',wfUpdate,{passive:true});

/* ---- close buttons on every subsection (2026-07-18): collapse THIS read and re-center it where it sat, so the page never becomes a mess of open sections ---- */
document.querySelectorAll('.acc.sub,.acc.qsub').forEach(a=>{const b=a.querySelector(':scope>.acc-panel>.inner>.acc-body');if(!b)return;const row=document.createElement('div');row.className='closerow';const btn=document.createElement('button');btn.className='nbtn';btn.innerHTML='<span class="triup" aria-hidden="true"></span>Close';btn.addEventListener('click',()=>{a.classList.remove('open');const t=a.querySelector(':scope>.acc-trigger');if(t)t.setAttribute('aria-expanded','false');const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;setTimeout(()=>a.scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'}),60);});row.appendChild(btn);b.appendChild(row);});

/* ==== DOCK BAR ==== */
(function(){
  /* Drop-UP menus for the dock bar. BLOCK COMMENTS ONLY in this file: Carrd
     publishes embed code flattened to a single line, so a line comment would
     comment out the rest of the program and the page would render blank.
     Capture phase on the buttons so a host page's own delegated handlers
     (Carrd's, and the book's anchor handler) cannot swallow the click. */
  var grps = [].slice.call(document.querySelectorAll('.dock-grp'));
  if (!grps.length) return;
  function closeAll(except){
    grps.forEach(function(g){
      if (g !== except){
        g.classList.remove('open');
        var b = g.querySelector('.dock-btn');
        if (b) b.setAttribute('aria-expanded','false');
      }
    });
  }
  grps.forEach(function(g){
    var b = g.querySelector('.dock-btn');
    if (!b) return;
    b.addEventListener('click', function(e){
      e.preventDefault();
      e.stopPropagation();
      var open = !g.classList.contains('open');
      closeAll(g);
      g.classList.toggle('open', open);
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    }, true);
  });
  document.addEventListener('click', function(){ closeAll(null); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape') closeAll(null); });
})();

/* Carrd hijacks hash navigation, so in-page # links scroll via JS instead
   (preventDefault keeps the hash from ever changing). data-open links already
   handle themselves (their element handler preventDefaults first). */
document.addEventListener('click',function(e){
  if(e.defaultPrevented)return;
  var a=e.target.closest('a[href^="#"]');
  if(!a)return;
  var el=document.getElementById(a.getAttribute('href').slice(1));
  if(!el)return;
  e.preventDefault();
  var y=el.getBoundingClientRect().top+window.scrollY-60;
  window.scrollTo({top:y,behavior:'smooth'});
});

/* ARRIVAL, not just clicks. A cross-site deep link (the dock's Resources menu,
   or any #id link from another page in the family) lands here as
   jcsjournals.com/#some-id, and Carrd swallows the native hash jump AND wipes
   the hash a moment later, so the reader sits at the top of the page with the
   target box below the fold. Measured on a 390 by 780 viewport: scrollY 0,
   box 454px down (the old #work-with-us box; the mechanism is generic).
   The hash is read immediately, at parse time, before Carrd can clear it, and
   the jump is INSTANT: a smooth animation over this distance gets interrupted. */
(function(){
  var wanted=(location.hash||'').slice(1);
  function land(id){
    if(!id)return;
    var el=document.getElementById(id);
    if(!el)return;
    var de=document.documentElement,prev=de.style.scrollBehavior;
    de.style.scrollBehavior='auto';
    window.scrollTo(0,el.getBoundingClientRect().top+window.scrollY-60);
    de.style.scrollBehavior=prev;
  }
  function run(){ land(wanted); setTimeout(function(){land(wanted);},350); }
  if(document.readyState==='complete')run();
  else window.addEventListener('load',run);
  window.addEventListener('hashchange',function(){ land((location.hash||'').slice(1)); });
})();
