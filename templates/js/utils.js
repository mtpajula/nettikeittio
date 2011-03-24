function nk_ajaxify_link(link, target) {

    var a = $(link);
    var url = a.attr("href");
    var contentdiv = $(target);
    a.click(function() {
        contentdiv.children().remove();
        contentdiv.append(
            $("<div />")
                .addClass("loading")
                .text("Loading")
        );
        
        
        $.ajax({
            type: "GET",
            url: url,
            success: function(data) {

                contentdiv.fadeOut('fast', function() {
                    contentdiv.fadeIn('fast').html(data);
                });
            }
        });

        return false; 
    });
}
