var freeBtn=document.getElementById('freeBtn'),freeDD=document.getElementById('freeDD');
freeBtn.addEventListener('click',function(ev){ev.stopPropagation();var o=freeDD.classList.contains('open');freeDD.classList.toggle('open',!o);freeBtn.setAttribute('aria-expanded',String(!o));});
freeDD.addEventListener('click',function(ev){ev.stopPropagation();});
document.querySelectorAll('[data-close-dd]').forEach(function(a){a.addEventListener('click',function(){freeDD.classList.remove('open');freeBtn.setAttribute('aria-expanded','false');});});
document.addEventListener('click',function(){freeDD.classList.remove('open');freeBtn.setAttribute('aria-expanded','false');});
document.querySelectorAll('.more-btn').forEach(function(b){
  b.addEventListener('click',function(){
    var x=document.getElementById(b.dataset.more);
    var open=x.classList.toggle('open');
    b.textContent=open?'show less':b.dataset.label;
  });
  b.dataset.label=b.textContent;
});
