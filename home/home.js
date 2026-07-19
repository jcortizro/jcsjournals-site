document.querySelectorAll('.arrow').forEach(function(b){
  b.addEventListener('click',function(){
    var rail=document.getElementById(b.dataset.rail);
    var card=rail.querySelector('.card');
    var step=card?card.offsetWidth+14:330;
    var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    rail.scrollBy({left:parseInt(b.dataset.dir,10)*step,behavior:reduce?'auto':'smooth'});
  });
});
