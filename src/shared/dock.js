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
