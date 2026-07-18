document.addEventListener('click',e=>{const t=e.target.closest('.acc-trigger');if(t){const acc=t.parentElement;const open=acc.classList.toggle('open');t.setAttribute('aria-expanded',open);if(acc.classList.contains('cat')&&open){document.querySelectorAll('.acc.cat.open').forEach(c=>{if(c!==acc)closeCat(c);});setTimeout(()=>{const y=acc.getBoundingClientRect().top+window.scrollY-70;window.scrollTo({top:y,behavior:'smooth'});},380);}}});
const dds=[['dietBtn','dietDD']];
dds.forEach(([b,d])=>{const btn=document.getElementById(b),dd=document.getElementById(d);btn.addEventListener('click',ev=>{ev.stopPropagation();const o=dd.classList.contains('open');document.querySelectorAll('.dropdown').forEach(x=>x.classList.remove('open'));dds.forEach(([b2])=>document.getElementById(b2).setAttribute('aria-expanded','false'));if(!o){dd.classList.add('open');btn.setAttribute('aria-expanded','true');}});});
document.querySelectorAll('.dd-cat').forEach(c=>c.addEventListener('click',ev=>{ev.stopPropagation();const subs=document.getElementById(c.dataset.subs);const open=subs.classList.contains('open');c.closest('.dropdown').querySelectorAll('.dd-subs').forEach(s=>s.classList.remove('open'));c.closest('.dropdown').querySelectorAll('.dd-cat').forEach(x=>x.setAttribute('aria-expanded','false'));if(!open){subs.classList.add('open');c.setAttribute('aria-expanded','true');}}));
document.addEventListener('click',()=>{document.querySelectorAll('.dropdown').forEach(x=>x.classList.remove('open'));dds.forEach(([b])=>document.getElementById(b).setAttribute('aria-expanded','false'));});
function openChain(id){let el=document.getElementById(id);if(!el)return;let node=el,topcat=null;while(node){if(node.classList&&node.classList.contains('acc')){node.classList.add('open');const tr=node.querySelector(':scope>.acc-trigger');if(tr)tr.setAttribute('aria-expanded','true');if(node.classList.contains('cat'))topcat=node;}node=node.parentElement;}if(topcat)document.querySelectorAll('.acc.cat.open').forEach(c=>{if(c!==topcat)closeCat(c);});setTimeout(()=>{const y=el.getBoundingClientRect().top+window.scrollY-70;window.scrollTo({top:y,behavior:'smooth'});},380);}
document.querySelectorAll('[data-open]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();openChain(a.dataset.open);}));
document.querySelectorAll('[data-close-dd]').forEach(a=>a.addEventListener('click',()=>document.querySelectorAll('.dropdown').forEach(x=>x.classList.remove('open'))));
if(location.hash){const id=location.hash.slice(1);if(document.getElementById(id))openChain(id);}
const modal=document.getElementById('legalModal'),mc=document.getElementById('modalContent');
const LEGAL={terms:`<h2>Terms of Use</h2><p class="eff">Effective 3/31/2026 · excerpt, full text loads from the live site</p><h3>Educational Nature</h3><p>All content is for educational and informational purposes only.</p><h3>External Links &amp; Recommendations</h3><p>This platform may direct you to books, programs, and membership platforms (Amazon, Mucus-Free Life). I don’t control them and am not responsible for their content, claims, or results. Some links may be affiliate links, I may earn a commission at no additional cost to you.</p><h3>Purchases</h3><p>Any purchases made through external platforms are governed by their terms, not mine.</p>`,medical:`<h2>Medical Disclaimer</h2><p class="eff">Effective 3/31/2026 · excerpt</p><h3>Educational Purpose Only</h3><p>Nothing here is medical advice, diagnosis, treatment, or a prescription. I am not a licensed medical professional; I share as a student. Always consult a qualified professional. No claims are made that any method cures disease, treats conditions, or produces guaranteed results.</p>`,privacy:`<h2>Privacy Policy</h2><p class="eff">Effective 3/31/2026 · excerpt</p><p>The free written information on this site can be read without an account, signup, or email address.</p>`};
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
else{go.innerHTML='Going further <span class="tri" aria-hidden="true"></span>';go.addEventListener('click',()=>{closeCat(cat);setTimeout(()=>{const y=document.getElementById('further').getBoundingClientRect().top+window.scrollY-60;window.scrollTo({top:y,behavior:'smooth'});},380);});}
row.appendChild(go);cat.appendChild(row);});
const wf=document.createElement('div');wf.className='wayfind';
wf.innerHTML='<button class="wf-top"><span class="triup" aria-hidden="true"></span>Topics</button><span class="wf-lbl"></span><button class="wf-next"></button>';
document.body.appendChild(wf);
const wfL=wf.querySelector('.wf-lbl'),wfN=wf.querySelector('.wf-next'),wfT=wf.querySelector('.wf-top');
let wfCat=null;
wfT.addEventListener('click',()=>goLibrary(wfCat));
wfN.addEventListener('click',()=>{if(!wfCat)return;const n=NEXT[wfCat.id];if(n)openChain(n);else{closeCat(wfCat);setTimeout(()=>{const y=document.getElementById('further').getBoundingClientRect().top+window.scrollY-60;window.scrollTo({top:y,behavior:'smooth'});},380);}});
function wfUpdate(){let cur=null;for(const c of CATS){if(!c.classList.contains('open'))continue;const r=c.getBoundingClientRect();if(r.top<-40&&r.bottom>innerHeight*.55){cur=c;break;}}
if(cur){wfCat=cur;wfL.innerHTML='<b>'+NUM[cur.id]+'</b>'+SHORT[cur.id];wfN.innerHTML=(NEXT[cur.id]?'Next':'Done')+' <span class="tri" aria-hidden="true"></span>';wf.classList.add('show');}
else{wf.classList.remove('show');wfCat=null;}}
addEventListener('scroll',wfUpdate,{passive:true});addEventListener('resize',wfUpdate,{passive:true});