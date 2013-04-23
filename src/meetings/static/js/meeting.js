"use strict";

$(function() {
    
    function toggleIssue(li, val, callback) {
        li.addClass('loading');
        $.post('', {
            issue : li.data('issue'),
            set : val
        }, function(data) {
            li.removeClass('loading');
        });
    }

    $(function() {

        $("#available").sortable({
            connectWith : "#upcoming",
            handle: "i",
            stop: function(event, ui){
                var to = ui.item.parent().attr("id");
                if (to == 'upcoming') {
                    toggleIssue(ui.item, 0);
                }
            }
        }).disableSelection();

        $("#upcoming").sortable({
            connectWith : "#available",
            handle: "i",
            stop: function(event, ui){
                var to = ui.item.parent().attr("id");
                if (to == 'available') {
                    toggleIssue(ui.item, 1);
                }
            }
        }).disableSelection();
    });

});
