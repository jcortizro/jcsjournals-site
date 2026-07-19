var freeBtn=document.getElementById('freeBtn'),freeDD=document.getElementById('freeDD');
freeBtn.addEventListener('click',function(ev){ev.stopPropagation();var o=freeDD.classList.contains('open');freeDD.classList.toggle('open',!o);freeBtn.setAttribute('aria-expanded',String(!o));});
freeDD.addEventListener('click',function(ev){ev.stopPropagation();});
document.querySelectorAll('.dd-cat').forEach(function(c){c.addEventListener('click',function(ev){ev.stopPropagation();var subs=document.getElementById(c.dataset.subs);var open=subs.classList.contains('open');freeDD.querySelectorAll('.dd-subs').forEach(function(s){s.classList.remove('open');});freeDD.querySelectorAll('.dd-cat').forEach(function(x){x.setAttribute('aria-expanded','false');});if(!open){subs.classList.add('open');c.setAttribute('aria-expanded','true');}});});
document.querySelectorAll('[data-close-dd]').forEach(function(a){a.addEventListener('click',function(){freeDD.classList.remove('open');freeBtn.setAttribute('aria-expanded','false');});});
document.addEventListener('click',function(){freeDD.classList.remove('open');freeBtn.setAttribute('aria-expanded','false');});
document.querySelectorAll('.arrow').forEach(function(b){
  b.addEventListener('click',function(){
    var rail=document.getElementById(b.dataset.rail);
    var card=rail.querySelector('.card');
    var step=card?card.offsetWidth+14:330;
    var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    rail.scrollBy({left:parseInt(b.dataset.dir,10)*step,behavior:reduce?'auto':'smooth'});
  });
});
