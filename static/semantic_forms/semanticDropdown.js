$(document).ready(function () {
  $(".ui.dropdown select")
    .not(".initialized")
    .not(".admin-autocomplete")
    .not("[name*=__prefix__]")
    .each(function () {
      $(this).dropdown({
        clearable: true,
        fullTextSearch: true,
        forceSelection: false, // https://github.com/Semantic-Org/Semantic-UI/issues/4506
      });
      $(this).addClass("initialized");
    });
});
