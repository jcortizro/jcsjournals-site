/* TD101 page script for jcsjournals.com. Runs once, after the Carrd loader has put jcj.html into #jcj-page. */

/* 0. Substack handoff (JC, 25 Oct 2026: "let's go the automated route"). The moment Kartra accepts an enrollment,
   this page also subscribes the same email to JC's Substack, exactly the way the old hub box did (Substack's own
   embed posts these fields to /api/v1/free). Kartra's script validates, then calls the form's native submit() and
   the browser navigates to Kartra; submit() fires no event, so the native method is wrapped, and a capture-phase
   submit listener covers the jQuery-trigger path. One handoff per form (data flag). keepalive lets the request
   finish while the page navigates away. Measured 25 Oct 2026: the fetch form of this request returns Substack's
   welcome redirect; a hidden-form POST from another origin returns 503. The visitor's consent is the fine print
   under the form ("and to subscribe to JC's email list"). Kartra's markup is never touched. */
(function(){
  var SUBSTACK='https://jcortizroman.substack.com/api/v1/free?nojs=true';
  var MARK='add_lead/cxUIOaN2t7dT';
  function handoff(form){
    try{
      if(!form||!form.action||form.action.indexOf(MARK)<0)return;
      if(form.getAttribute('data-jcj-handoff')==='1')return;
      var el=form.querySelector('input[name="email"]');
      var email=el?String(el.value||'').trim():'';
      if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))return;
      form.setAttribute('data-jcj-handoff','1');
      var here=location.href.split('#')[0];
      var body=new URLSearchParams({first_url:here,first_referrer:'',current_url:here,current_referrer:'',
        first_session_url:here,first_session_referrer:'',referral_code:'',source:'embed',
        referring_pub_id:'',additional_referring_pub_ids:'',email:email});
      if(window.fetch){fetch(SUBSTACK,{method:'POST',mode:'no-cors',credentials:'omit',keepalive:true,body:body}).catch(function(){});}
    }catch(e){}
  }
  var nativeSubmit=HTMLFormElement.prototype.submit;
  HTMLFormElement.prototype.submit=function(){handoff(this);return nativeSubmit.apply(this,arguments);};
  document.addEventListener('submit',function(e){handoff(e.target);},true);
})();

/* 1. Spira's Kartra form. Script tags that arrive through innerHTML never run, so each Kartra tag is
   re-created as a real script element at the same spot. Kartra then draws its form right after it,
   inside the same .kslot. The page's address (kuid, kref, lid, utm_) is left alone: Kartra reads those
   on load and removes them itself, and that is what credits a sign-up to JC's link. */
(function(){
  var page=document.getElementById('jcj-page');
  if(!page)return;
  var tags=page.querySelectorAll('script[src*="app.kartra.com/optin/"]');
  Array.prototype.forEach.call(tags,function(old){
    var s=document.createElement('script');
    s.src=old.getAttribute('src');
    old.parentNode.insertBefore(s,old);
    old.parentNode.removeChild(old);
  });
})();

/* 2. Carrd hijacks hash navigation, so in-page # links (every "Enroll me free" button points at #enroll)
   scroll via JS instead. preventDefault keeps the hash from ever changing. Same fix the hub uses. */
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

/* 3. Arrival on jcsjournals.com/#enroll: Carrd swallows the native jump and wipes the hash, so the hash
   is read at parse time and the jump is instant. Same fix the hub uses. */
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

/* 4. Top-right menu (JC, 25 Oct 2026). "Free resources" + the three lines open the side panel; the X, the dark
   backdrop and Escape close it. "Socials" opens and closes its own list of four channels. */
(function(){
  var root=document.documentElement;
  var btn=document.querySelector('#jcj-page .navbtn');
  var panel=document.getElementById('jcj-menu');
  if(!btn||!panel)return;
  function isOpen(){return root.classList.contains('jcj-nav-open');}
  function setOpen(on){
    root.classList.toggle('jcj-nav-open',on);
    btn.setAttribute('aria-expanded',on?'true':'false');
    var target=on?panel.querySelector('.navclose'):btn;
    if(target)try{target.focus({preventScroll:true});}catch(e){}
  }
  btn.addEventListener('click',function(){setOpen(!isOpen());});
  Array.prototype.forEach.call(document.querySelectorAll('#jcj-page [data-navclose]'),function(el){
    el.addEventListener('click',function(){setOpen(false);});
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&isOpen())setOpen(false);});
  var soc=panel.querySelector('.navsoc'),sub=document.getElementById('jcj-socials');
  if(soc&&sub)soc.addEventListener('click',function(){
    var on=soc.getAttribute('aria-expanded')!=='true';
    soc.setAttribute('aria-expanded',on?'true':'false');
    sub.hidden=!on;
  });
})();
