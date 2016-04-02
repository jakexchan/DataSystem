(function(){
    var flip_dom_lists = $('.flip'),
        list_show_lists = $('.list-show');

    $('.flip').each(function(){
        $(this).click(function(){
            $(this).next('.list-show').slideToggle();
        });
    });

    $('.list-show li').mouseover(function(){
        $(this).addClass('active');
    });
    $('.list-show li').mouseout(function(){
        $(this).removeClass('active');
    });
}());