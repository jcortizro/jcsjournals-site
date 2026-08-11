(function () {
  // Nothing may ever clip. Shrink a page's type until its content fits, and
  // report the result so a bad page cannot hide.
  // Measuring scrollHeight against a fixed-ratio flex box lies twice over:
  // flex children shrink to hide overflow, and margin-top:auto makes a short
  // page report as exactly full. So measure the page UNCONSTRAINED and compare
  // its natural height to the height the 8.5x11 ratio actually allows.
  var PROBE = document.createElement('style');
  PROBE.textContent =
    '.page.is-measuring{aspect-ratio:auto!important;height:auto!important;overflow:visible!important}' +
    '.page.is-measuring > *{flex-shrink:0!important}' +
    '.page.is-measuring .folio,.page.is-measuring .cta-bar,.page.is-measuring .r-notes{margin-top:.7em!important}';
  var SAFETY = 6;

  function naturalHeight(page) {
    page.classList.add('is-measuring');
    var h = page.scrollHeight;
    page.classList.remove('is-measuring');
    return h;
  }

  function fit(page) {
    var targetH = page.parentElement.clientWidth * 11 / 8.5;
    // Front matter carries far less content than a recipe page, so starting it at
    // the recipe size leaves the bottom half empty. Start those pages larger and
    // let the same shrink loop settle them. Recipe pages still start at 2.14, so
    // JC's approved spread is byte-for-byte unchanged.
    var start = page.classList.contains('fm') ? 3.10 : 2.14;
    var scale = start, guard = 0;
    page.style.fontSize = scale + 'cqw';
    while (naturalHeight(page) > targetH - SAFETY && scale > 1.30 && guard < 80) {
      scale -= 0.03;
      page.style.fontSize = scale.toFixed(2) + 'cqw';
      guard++;
    }
    return { fits: naturalHeight(page) <= targetH, scale: scale };
  }

  function run() {
    var pages = Array.prototype.slice.call(document.querySelectorAll('.page'));
    document.head.appendChild(PROBE);
    var bad = [], tight = [];
    pages.forEach(function (p, i) {
      var r = fit(p);
      if (!r.fits) bad.push(i + 1);
      else if (r.scale < 1.80) tight.push({ page: i + 1, scale: +r.scale.toFixed(2) });
    });
    PROBE.remove();
    window.__bookFit = { total: pages.length, overflowing: bad, tight: tight };
  }
  if (document.readyState === 'complete') run();
  else window.addEventListener('load', run);
  window.addEventListener('resize', function () { clearTimeout(window.__t); window.__t = setTimeout(run, 200); });

  // Carrd hijacks hash navigation, so inside a Carrd embed every href="#x"
  // silently does nothing (proven live on the td101landing embed, and the same
  // trap the jcj page hit). Delegated handler + scrollIntoView works in both
  // homes: standalone GitHub Pages and the Carrd shell. Capture phase, so this
  // wins even if the host page has its own delegated click handlers.
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[data-t], a[href^="#"]') : null;
    if (!a) return;
    // data-t first: on the Carrd surface the loader strips these anchors'
    // hrefs so Carrd's own hash handling never sees the click at all (its
    // handler animates back to the section top and undoes any jump we make).
    // On GitHub Pages / the PDF the hrefs stay and native behavior is fine.
    var id = a.getAttribute('data-t') || (a.getAttribute('href') || '').slice(1);
    if (!id) return;
    var t = document.getElementById(id);
    if (!t) return;
    e.preventDefault();
    e.stopPropagation();
    // Instant, never smooth: on this 44k px page smooth animation gets
    // interrupted and strands the reader between pages. And 'auto' is NOT
    // instant, it defers to the css scroll-behavior, which the site shell
    // sets to smooth. So: force the css off for the jump, use 'instant',
    // then restore. Measured live on the Carrd embed, lands at exactly 0.
    var de = document.documentElement;
    var prev = de.style.scrollBehavior;
    de.style.scrollBehavior = 'auto';
    t.scrollIntoView({ behavior: 'instant', block: 'start' });
    de.style.scrollBehavior = prev;
  }, true);
})();