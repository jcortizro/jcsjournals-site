document.querySelectorAll('.more-btn').forEach(function(b){
  b.addEventListener('click',function(){
    var x=document.getElementById(b.dataset.more);
    var open=x.classList.toggle('open');
    b.textContent=open?'show less':b.dataset.label;
  });
  b.dataset.label=b.textContent;
});

/* ==== LIBRARY engine ==== */
document.addEventListener('click',e=>{const t=e.target.closest('.acc-trigger');if(t){const acc=t.parentElement;const open=acc.classList.toggle('open');t.setAttribute('aria-expanded',open);if(acc.classList.contains('cat')&&open){document.querySelectorAll('.acc.cat.open').forEach(c=>{if(c!==acc)closeCat(c);});setTimeout(()=>{const y=acc.getBoundingClientRect().top+window.scrollY-70;window.scrollTo({top:y,behavior:'smooth'});},380);}}});




function openChain(id){let el=document.getElementById(id);if(!el)return;let node=el,topcat=null;while(node){if(node.classList&&node.classList.contains('acc')){node.classList.add('open');const tr=node.querySelector(':scope>.acc-trigger');if(tr)tr.setAttribute('aria-expanded','true');if(node.classList.contains('cat'))topcat=node;}node=node.parentElement;}if(topcat)document.querySelectorAll('.acc.cat.open').forEach(c=>{if(c!==topcat)closeCat(c);});setTimeout(()=>{const y=el.getBoundingClientRect().top+window.scrollY-70;window.scrollTo({top:y,behavior:'smooth'});},380);}
document.querySelectorAll('[data-open]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();openChain(a.dataset.open);}));
document.querySelectorAll('[data-close-dd]').forEach(a=>a.addEventListener('click',()=>document.querySelectorAll('.dropdown').forEach(x=>x.classList.remove('open'))));
if(location.hash){const id=location.hash.slice(1);if(document.getElementById(id))openChain(id);}
const modal=document.getElementById('legalModal'),mc=document.getElementById('modalContent');
const LEGAL={terms:`
<h2>Terms of Use</h2><p class="eff">Effective Date: 2/25/2026</p>
<p>Welcome to this website (jcsjournals.com). By accessing or using this Site, you agree to the following Terms of Use. If you do not agree, please do not use the Site.</p>
<h3>Introduction</h3>
<p>By accessing or using this website (jcsjournals.com), you agree to the following Terms of Use. If you do not agree with these Terms, you must not use this Site. This Site is independently operated and is not the official website of Mucus-Free Life LLC and/or Eden Ministries Trust.</p>
<h3>Educational Purpose Only</h3>
<p>The content on this Site, including videos, written material, and links, is provided strictly for informational and educational purposes. The information shared relates to perspectives on health, the Mucusless Diet Healing System, and the teachings of Prof. Arnold Ehret. It is not medical advice, medical diagnosis, treatment, or a substitute for consultation with a licensed healthcare professional. Nothing on this Site creates a doctor-patient relationship or healthcare provider relationship. If you choose to apply any information presented here, you do so voluntarily and at your own discretion.</p>
<h3>Assumption of Risk</h3>
<p>By using this Site, you acknowledge that dietary and lifestyle changes involve inherent risks. You assume full responsibility for any actions you take based on the information presented on this Site. The owner of this Site is not responsible for any outcomes resulting from your personal decisions.</p>
<h3>Affiliation Disclosure</h3>
<p>The owner of this Site is affiliated with Mucus-Free Life and appears in its educational materials, including the Transition Diet 101 course. However:</p>
<ul><li>This Site does not sell products or services.</li><li>This Site does not collect payments.</li><li>This Site does not manage memberships or user accounts.</li><li>This Site does not control or operate Mucus-Free Life platforms.</li></ul>
<p>All courses, memberships, email lists, products, and services referenced through external links are independently operated by Mucus-Free Life LLC and/or Eden Ministries Trust and are governed by their own terms and policies.</p>
<h3>External Links</h3>
<p>This Site contains links to third-party websites. The owner of this Site is not responsible for the content, policies, practices, or transactions conducted on any external website. Visiting those websites is done at your own discretion.</p>
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
<p>To the fullest extent permitted by law, the owner of this Site shall not be liable for any direct, indirect, incidental, consequential, special, or business-related losses arising from the use of this Site or reliance on its content. These limitations apply even if the possibility of such damages has been advised. Nothing in these Terms excludes liability where it would be unlawful to do so.</p>
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
<h2>Medical Disclaimer</h2><p class="eff">Effective Date: 3/31/2026</p>
<p>Welcome to this website (jcsjournals.com). This Medical Disclaimer applies to all content on this Site.</p>
<h3>1. Educational Purpose Only</h3>
<p>The content shared on this platform is for educational and informational purposes only. This includes:</p>
<ul><li>Articles</li><li>Visual content</li><li>Menu examples</li><li>Explanations of the Mucusless Diet Healing System (MDHS)</li></ul>
<p>All material reflects:</p>
<ul><li>Personal study</li><li>Interpretation of existing teachings</li><li>Educational exploration</li></ul>
<p>This content is not intended as medical advice.</p>
<h3>2. Not Medical Advice</h3>
<p>Nothing on this platform should be interpreted as:</p>
<ul><li>Medical advice</li><li>Diagnosis</li><li>Treatment recommendation</li><li>Health prescription</li></ul>
<p>I am not a licensed medical professional. I share as a student documenting my learning and understanding of concepts originally developed by Arnold Ehret and interpreted through modern application. Always consult a qualified healthcare professional before making decisions related to your health.</p>
<h3>3. No Doctor&ndash;Patient Relationship</h3>
<p>Using this website, consuming content, or interacting with any materials does not create a doctor&ndash;patient relationship. No individualized guidance is being provided.</p>
<h3>4. Health &amp; Wellness Information</h3>
<p>This platform discusses topics including:</p>
<ul><li>Diet and food selection</li><li>Fasting and juice consumption</li><li>Elimination processes</li><li>Natural lifestyle practices</li></ul>
<p>These topics are presented within a historical and educational framework. No statements made on this platform are intended to:</p>
<ul><li>Diagnose conditions</li><li>Treat illness</li><li>Cure disease</li><li>Prevent medical issues</li></ul>
<h3>5. Personal Responsibility</h3>
<p>By using this platform, you acknowledge and agree that:</p>
<ul><li>You are responsible for your own health decisions</li><li>You apply any information at your own discretion</li><li>You understand that results vary between individuals</li></ul>
<p>You assume full responsibility for any actions taken based on the information provided.</p>
<h3>6. No Guarantees</h3>
<p>No guarantees are made regarding:</p>
<ul><li>Results</li><li>Outcomes</li><li>Health improvements</li></ul>
<p>Any examples shared (including menus, experiences, or observations) are:</p>
<ul><li>Illustrative</li><li>Educational</li><li>Not predictive of your experience</li></ul>
<h3>7. Sensitive Practices Disclaimer</h3>
<p>Some content may reference practices such as:</p>
<ul><li>Fasting</li><li>Dietary transitions</li><li>Elimination-related experiences</li></ul>
<p>These can affect individuals differently. This platform does not recommend that any specific person engage in these practices. Decisions regarding such practices should be made with appropriate professional guidance.</p>
<h3>8. External Resources</h3>
<p>This platform may reference or link to external materials, including:</p>
<ul><li>Books</li><li>Programs</li><li>Membership platforms</li><li>Third-party websites</li></ul>
<p>These are shared for educational purposes. I do not control and am not responsible for:</p>
<ul><li>Their claims</li><li>Their recommendations</li><li>Their outcomes</li></ul>
<h3>9. Emergency Notice</h3>
<p>If you are experiencing a medical emergency: Seek immediate help from a licensed medical professional or emergency services. Do not rely on information from this platform.</p>
`,privacy:`
<h2>Privacy Policy</h2><p class="eff">Effective Date: 3/31/2026</p>
<p>Welcome to this website (jcsjournals.com). This Privacy Policy explains what information is, and is not, collected when you use this Site.</p>
<h3>1. Overview</h3>
<p>This website is designed to share educational content related to the Mucusless Diet Healing System (MDHS). I value simplicity and transparency. I do not actively collect personal information such as names or email addresses on this site.</p>
<h3>2. Information Automatically Collected</h3>
<p>Like most websites, some basic information may be collected automatically when you visit, including:</p>
<ul><li>IP address</li><li>Browser type</li><li>Device type</li><li>Pages visited</li></ul>
<p>This data is used for general website functionality and performance. I do not use this information to personally identify you.</p>
<h3>3. No Direct Data Collection</h3>
<p>This website does not:</p>
<ul><li>Require account creation</li><li>Collect email addresses</li><li>Store personal user profiles</li></ul>
<p>You can browse freely without submitting personal information.</p>
<h3>4. External Links</h3>
<p>This site may direct you to external platforms, including:</p>
<ul><li>Amazon</li><li>Mucus-Free Life membership platform</li></ul>
<p>If you choose to visit these platforms, they may collect personal information such as:</p>
<ul><li>Name</li><li>Email address</li><li>Payment information</li></ul>
<p>These platforms operate independently and have their own privacy policies. I am not responsible for how they collect, use, or store your data.</p>
<h3>5. Cookies &amp; Tracking</h3>
<p>This site may use basic cookies or analytics tools to:</p>
<ul><li>Understand general traffic patterns</li><li>Improve site performance</li></ul>
<p>These tools do not personally identify you.</p>
<h3>6. Your Choice</h3>
<p>You can choose to:</p>
<ul><li>Leave the site at any time</li><li>Avoid clicking external links</li><li>Disable cookies through your browser settings</li></ul>
<h3>7. Changes to This Policy</h3>
<p>This Privacy Policy may be updated at any time. Continued use of the site means you accept the latest version.</p>
`};
document.querySelectorAll('[data-modal]').forEach(b=>b.addEventListener('click',()=>{mc.innerHTML=LEGAL[b.dataset.modal];modal.showModal();}));
modal.addEventListener('click',e=>{if(e.target===modal||e.target.closest('[data-close]'))modal.close();});

/* ---- next-topic rows + sticky wayfinder (2026-07-17) ---- */
function closeCat(c){c.classList.remove('open');const t=c.querySelector(':scope>.acc-trigger');if(t)t.setAttribute('aria-expanded','false');}
const CATS=[...document.querySelectorAll('.acc.cat')];
const NUM={};CATS.forEach((c,i)=>NUM[c.id]=i+1);
const NEXT={foundation:'menus',menus:'mechanics',mechanics:'enemas',enemas:'addiction',addiction:'faq',faq:null};
const SHORT={foundation:'What Is the MDHS?',menus:'Learn What to Eat',mechanics:'Learn How to Eat',enemas:'Waste Eliminator',addiction:'Addiction & Relapse',faq:'FAQ'};
function goLibrary(cat){if(cat)closeCat(cat);setTimeout(()=>{const y=document.getElementById('library').getBoundingClientRect().top+window.scrollY-60;window.scrollTo({top:y,behavior:'smooth'});},380);}
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
