"use strict";

$(function() {

    function toggleIssue(li, val, callback) {
        $.post('', {
            issue : li.data('issue'),
            set : val
        }, function(data) {
            li.removeClass('loading');
        });
    }

    $('#agenda').on('click', '.addremove', function() {
        $(this).find('.ui-icon-minus').removeClass('ui-icon-minus').addClass('ui-icon-plus');
        var el = $(this).parent();
        $("#available").append(el);
        toggleIssue(el, 1);
    });

    $('#available').on('click', '.addremove', function() {
        $(this).find('.ui-icon-plus').removeClass('ui-icon-plus').addClass('ui-icon-minus');
        var el = $(this).parent();
        $("#agenda").append(el);
        toggleIssue(el, 0);
    });


});
