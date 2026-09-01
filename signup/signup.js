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
const LEGAL={terms:`<h2>Terms of Use</h2><p class="eff">Effective 3/31/2026 · excerpt, full text loads from the live site</p><h3>Educational Nature</h3><p>All content is for educational and informational purposes only.</p><h3>External Links &amp; Recommendations</h3><p>This platform may direct you to books, programs, and membership platforms (Amazon, Mucus-Free Life). I don’t control them and am not responsible for their content, claims, or results. Some links may be affiliate links, I may earn a commission at no additional cost to you.</p><h3>Purchases</h3><p>Any purchases made through external platforms are governed by their terms, not mine.</p>`,medical:`<h2>Medical Disclaimer</h2><p class="eff">Effective 3/31/2026 · excerpt</p><h3>Educational Purpose Only</h3><p>Nothing here is medical advice, diagnosis, treatment, or a prescription. I am not a licensed medical professional; I share as a student. Always consult a qualified professional. No claims are made that any method cures disease, treats conditions, or produces guaranteed results.</p>`,privacy:`<h2>Privacy Policy</h2><p class="eff">Effective 3/31/2026 · excerpt</p><p>The free written information on this site can be read without an account, signup, or email address.</p>`};
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
else{go.innerHTML='Explore the paid services <span class="tri" aria-hidden="true"></span>';go.addEventListener('click',()=>{closeCat(cat);setTimeout(()=>{window.location.href='https://jcsjournals.com/#paid';},380);});}
row.appendChild(go);cat.appendChild(row);});
const wf=document.createElement('div');wf.className='wayfind';
wf.innerHTML='<button class="wf-top"><span class="triup" aria-hidden="true"></span>Topics</button><span class="wf-lbl"></span><button class="wf-next"></button>';
document.body.appendChild(wf);
const wfL=wf.querySelector('.wf-lbl'),wfN=wf.querySelector('.wf-next'),wfT=wf.querySelector('.wf-top');
let wfCat=null;
wfT.addEventListener('click',()=>goLibrary(wfCat));
wfN.addEventListener('click',()=>{if(!wfCat)return;const n=NEXT[wfCat.id];if(n)openChain(n);else{closeCat(wfCat);setTimeout(()=>{window.location.href='https://jcsjournals.com/#paid';},380);}});
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


/* ==== SIGNUP ==== */
(function () {
  /* Waitlist submit. Posts first name, last name and email to a Google Apps
     Script web app, which appends a row to JC's sheet.

     BLOCK COMMENTS ONLY in this file: it ships inside a Carrd embed, and Carrd
     publishes embed code flattened to one line, so a line comment would
     comment out the rest of the program.

     The POST is sent as form-encoded with no custom headers, which keeps it a
     CORS "simple request": Apps Script does not answer preflight OPTIONS, so
     anything fancier fails in the browser even when the script is fine. */
  var ENDPOINT = 'https://script.google.com/macros/s/AKfycbwMB9tFEhlSdP5zpY1MEDUTvF0-anUUuwQOO-0CIk39LaaeSz305yXzFldeNwGK-Sw4/exec';

  var form = document.getElementById('waitform');
  var done = document.getElementById('signdone');
  var err = document.getElementById('ferr');
  var btn = document.getElementById('fsubmit');
  if (!form) return;

  function fail(msg, field) {
    err.textContent = msg;
    err.hidden = false;
    if (field) { field.setAttribute('aria-invalid', 'true'); field.focus(); }
  }

  function clearErr() {
    err.hidden = true;
    [].forEach.call(form.querySelectorAll('input'), function (i) { i.removeAttribute('aria-invalid'); });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearErr();
    var first = form.first.value.trim();
    var last = form.last.value.trim();
    var email = form.email.value.trim();

    if (!first) return fail('Please add your first name.', form.first);
    if (!last) return fail('Please add your last name.', form.last);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) return fail('That email does not look right.', form.email);

    if (!ENDPOINT || ENDPOINT.indexOf('__') === 0) {
      return fail('The waitlist is not connected yet. Please try again a little later.');
    }

    btn.disabled = true;
    btn.textContent = 'Sending...';

    var body = new URLSearchParams();
    body.set('first', first);
    body.set('last', last);
    body.set('email', email);
    body.set('source', location.hostname);

    fetch(ENDPOINT, { method: 'POST', body: body })
      .then(function (r) { if (!r.ok) throw new Error('bad status'); return r.text(); })
      .then(function () {
        form.hidden = true;
        done.hidden = false;
        done.scrollIntoView({ block: 'nearest' });
      })
      .catch(function () {
        btn.disabled = false;
        btn.textContent = 'Join The Waitlist';
        fail('That did not go through. Please check your connection and try once more.');
      });
  });
})();

