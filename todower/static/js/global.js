$( ".alert" ).each(function(index) {
    var time = 2500;
    $(this).delay(time*(index+1)).fadeOut(400);
});