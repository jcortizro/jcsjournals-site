document.querySelectorAll('.more-btn').forEach(function(b){
  b.addEventListener('click',function(){
    var x=document.getElementById(b.dataset.more);
    var open=x.classList.toggle('open');
    b.textContent=open?'show less':b.dataset.label;
  });
  b.dataset.label=b.textContent;
});
