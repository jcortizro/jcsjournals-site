
(function(){
  var FLOWS = ["noapp","circleapp","desktop"];
  var SUBS = {noapp:"On your phone, no app needed. Scroll down and do one picture at a time.",circleapp:"On your phone, with the Circle app. Scroll down and do one picture at a time.",desktop:"On a computer. Scroll down and do one picture at a time."};
  var LABELS = {noapp:"YOU ARE ON: PHONE, NO APP",circleapp:"YOU ARE ON: PHONE, CIRCLE APP",desktop:"YOU ARE ON: COMPUTER"};
  var CHOOSE_SUB = "First, tell us what you are using. Then you only see your own steps.";
  var root = document.documentElement;
  var wrap = document.querySelector(".wrap");
  var chooser = document.getElementById("chooser");
  var foot = document.getElementById("foot");
  var bar = document.getElementById("youare");
  var ylab = document.getElementById("ylab");
  var yicon = document.getElementById("yicon");
  var sub = document.querySelector(".herosub");

  function accentClass(flow){
    for (var i = 0; i < FLOWS.length; i++) root.classList.remove("f-" + FLOWS[i]);
    if (flow) root.classList.add("f-" + flow);
  }

  function show(flow, writeUrl){
    for (var i = 0; i < FLOWS.length; i++){
      var el = document.getElementById("flow-" + FLOWS[i]);
      if (el) el.hidden = (FLOWS[i] !== flow);
    }
    chooser.hidden = !!flow;
    if (foot) foot.hidden = !flow;
    bar.hidden = !flow;
    accentClass(flow);
    if (flow){
      ylab.textContent = LABELS[flow];
      var src = document.querySelector(".pick-" + flow + " svg");
      yicon.innerHTML = "";
      if (src) yicon.appendChild(src.cloneNode(true));
      if (sub) sub.textContent = SUBS[flow];
    } else if (sub) {
      sub.textContent = CHOOSE_SUB;
    }
    if (writeUrl){
      try {
        history.replaceState(null, "", flow ? "?flow=" + flow : location.pathname);
      } catch (e) {}
    }
    window.scrollTo(0, 0);
  }

  var picks = document.querySelectorAll(".pick");
  for (var i = 0; i < picks.length; i++){
    picks[i].addEventListener("click", function(){
      show(this.getAttribute("data-flow"), true);
    });
  }
  document.getElementById("yswitch").addEventListener("click", function(){
    show(null, true);
  });

  var want = null;
  try { want = (new URLSearchParams(location.search)).get("flow"); } catch (e) {}
  if (!want && location.hash) want = location.hash.slice(1);
  show(FLOWS.indexOf(want) === -1 ? null : want, FLOWS.indexOf(want) !== -1);
})();
