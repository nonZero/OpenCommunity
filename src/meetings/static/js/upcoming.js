"use strict";

$(function() {

    function toggleIssue(li, val, callback) {
        $.post('', {
            issue : li.data('issue'),
            set : val
        }, function(data) {
            li.removeClass('loading');
        }).fail(function() {
            alert('Server Error. Please refresh your browser and try again');
        });
    }

    $('#agenda').on('click', '.addremove', function() {
        $(this).find('.ui-icon-minus').removeClass('ui-icon-minus').addClass('ui-icon-plus');
        var el = $(this).parent();
        el.addClass('loading');
        $("#available").append(el);
        toggleIssue(el, 1);
    });

    $('#available').on('click', '.addremove', function() {
        $(this).find('.ui-icon-plus').removeClass('ui-icon-plus').addClass('ui-icon-minus');
        var el = $(this).parent();
        el.addClass('loading');
        $("#agenda").append(el);
        toggleIssue(el, 0);
    });


});
