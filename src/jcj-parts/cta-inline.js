/* Sprinkles a compact "work with us" strip at the end of every library topic,
   just above that topic's All-topics / Next row, so it lands where a reader
   actually finishes reading. Copy varies per topic so six of them don't read
   as the same banner repeated. */
(function(){
  var CTA_URL='https://calendly.com/team-mucusfreelife/15-minute-clarity-call';
  var LINES={
    foundation:'Want to know what this looks like applied to your own body?',
    menus:'Not sure what any of this looks like on your plate, in your life?',
    mechanics:'Want help running this at your own pace, with your own schedule?',
    enemas:'Have questions you would rather ask a person than a web page?',
    addiction:'Working through this on your own is hard. You do not have to.',
    faq:'Still have a question this page did not answer?'
  };
  document.querySelectorAll('.acc.cat').forEach(function(cat){
    var line=LINES[cat.id];if(!line)return;
    var box=document.createElement('div');
    box.className='ctamini';
    box.innerHTML='<span class="cm-t">'+line+'<span class="cm-s">Get in contact with our team and learn about the services we provide.</span></span>'+
      '<a class="btn green cm-b" href="'+CTA_URL+'" target="_blank" rel="noopener">Free 15-Min Call</a>';
    var row=cat.querySelector(':scope>.nextrow');
    if(row)cat.insertBefore(box,row);else cat.appendChild(box);
  });
})();