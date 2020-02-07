jQuery(document).ready(function($) {
    // hide the menu when the page load
    $("#navigation-list").hide();
    // when .menuBtn is clicked, do this
    $(".menuBtn").click(function() {
    // open the menu with slide effect
    $("#navigation-list").slideToggle(300);
    });
    });