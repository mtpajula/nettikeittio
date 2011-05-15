
$(document).ready(function () {
    // Kulmien pyöristys
    $('#content').corner();
    $('.listresult').corner();
    $('.listDiv').corner();
    $('#menu .menulist').corner("bottom");
    $('#menuHeader .menulist:first-child').corner("tl");
    $('#menuHeader .menulist:last-child').corner("tr");
    $('.phase, .phase_name, .phase_dscr, .phase_ingredients').corner();
    $(".detailIngredients").corner();
});
