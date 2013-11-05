"use strict";

$(function() {

    function reorderIssues(li, val, callback) {
        $('#agenda-container').addClass('loading');
        var l = $('#agenda li').map(function() {
            return $(this).data('issue');
        }).get();
        $.post('', {
            issues : l,
        }, function(data) {
            $('#agenda-container').removeClass('loading');
        }).fail(function() {
            alert('Server Error. Please refresh your browser and try again');
        });
    }

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
        //$(this).find('.icon-minus').removeClass('icon-minus').addClass('icon-plus');
        var el = $(this).parent().parent();
        el.addClass('loading');
        //console.log(el)
        $("#available").append(el);
        toggleIssue(el, 1);
    }).sortable({
        'containment': $('#agenda').parent().parent(),
        'opacity': 0.6,
        cursorAt: { top: 25 },
        handle: ".grab",
        update: function(event, ui) {
            reorderIssues();
        }
    }).removeClass('ui-corner-all').filter('li').removeClass('ui-corner-bottom');

    $('#available').on('click', '.addremove', function() {
        //$(this).find('.icon-plus').removeClass('icon-plus').addClass('icon-minus');
        var el = $(this).parent().parent();
        el.addClass('loading');
        $("#agenda").append(el);
        toggleIssue(el, 0);
    });

    $('#agenda').on('click', '.timer span', function() {
        $(this).hide();
        var v = $(this).data('strict');
        if (v == "") {
            v = '00:00';
        }
        $(this).parent().append($('<input type="time" step="300" class="x" value="'+v+'"/><button>Save</button>'));
    });

    $('#agenda').on('click', '.timer button', function() {
        var el = $(this).parent();
        var v = el.find('.x').val();
        el.find('input,button').detach();
        el.find('span').html('...').data('strict', v).show();
        $.post(el.data('url'), {length: v}, function(data) {
            el.find('span').text(data);
        });
    });


});
