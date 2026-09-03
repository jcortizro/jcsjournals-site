
(function(){
  var subs = {
    noapp: 'On your phone, no app needed. Scroll down and do one picture at a time.',
    circleapp: 'On your phone, with the Circle app. Scroll down and do one picture at a time.'
  };
  function show(which){
    var other = which === "noapp" ? "circleapp" : "noapp";
    document.getElementById("flow-" + which).hidden = false;
    document.getElementById("flow-" + other).hidden = true;
    document.getElementById("btn-" + which).setAttribute("aria-pressed", "true");
    document.getElementById("btn-" + other).setAttribute("aria-pressed", "false");
    var s = document.querySelector(".herosub");
    if (s) s.textContent = subs[which];
    history.replaceState(null, "", "?flow=" + which);
    window.scrollTo(0, 0);
  }
  document.getElementById("btn-noapp").addEventListener("click", function(){ show("noapp"); });
  document.getElementById("btn-circleapp").addEventListener("click", function(){ show("circleapp"); });
  var q = (new URLSearchParams(location.search)).get("flow");
  if (q === "circleapp" || location.hash === "#circleapp") show("circleapp");
})();
