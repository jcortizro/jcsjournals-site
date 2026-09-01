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