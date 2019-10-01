(function($) {
    var star = {
        add: '<span class="glyphicon glyphicon-star"></span>',
        remove: '<span class="glyphicon glyphicon-star-empty"></span>'
    };

    $(document).on("click", ".like-button", function() {
        var $button = $(this);
        var $widget = $button.closest(".like-widget");
        var $badge = $widget.find(".like-badge");

        $.post($button.data("href"), function(data) {
            if (data.success) {
                var action = data.action; // "add" or "remove"
                var label = $button.data(action + "-label");


                $button[action + "Class"]("active");
                $button.html(star[action] + " " + label);

                $badge.html(data.count);
            }
        }, "json");
    });
}(jQuery));
