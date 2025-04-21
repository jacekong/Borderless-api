$(document).ready(function () {
  $(".ui.checkbox")
    .not(".initialized")
    .not("[name*=__prefix__]")
    .each(function () {
      $(this).checkbox();
      $(this).addClass("initialized");
    });
});
