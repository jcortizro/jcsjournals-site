(function () {
  /* Retired 2026-09-02. This module used to post the waitlist form (first name,
     last name, email) to a Google Apps Script web app that appended a row to
     JC's sheet. On 2026-09-01 the form was replaced by Substack's official
     embedded sign-up (the only subscribe path Substack accepts), so this site
     no longer sends visitor data anywhere, and the privacy policy now promises
     exactly that. The module is retired rather than left dormant so the shipped
     bundle contains no collection endpoint and matches the policy. The old
     implementation lives in git history (see src/signup/signup.js before this
     date) if a first-party form ever returns.

     BLOCK COMMENTS ONLY in this file: it ships inside a Carrd embed, and Carrd
     publishes embed code flattened to one line, so a line comment would
     comment out the rest of the program. */
})();
