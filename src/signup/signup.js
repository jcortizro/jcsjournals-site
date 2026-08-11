(function () {
  /* Waitlist submit. Posts first name, last name and email to a Google Apps
     Script web app, which appends a row to JC's sheet.

     BLOCK COMMENTS ONLY in this file: it ships inside a Carrd embed, and Carrd
     publishes embed code flattened to one line, so a line comment would
     comment out the rest of the program.

     The POST is sent as form-encoded with no custom headers, which keeps it a
     CORS "simple request": Apps Script does not answer preflight OPTIONS, so
     anything fancier fails in the browser even when the script is fine. */
  var ENDPOINT = '__FORMENDPOINT__';

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
