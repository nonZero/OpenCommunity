"use strict";

$(function() {

    function toggleProposal(li) {
        li.addClass('loading');
        $.post(li.find('a').attr('href'), {
            issue : li.data('id'),
            accepted : li.data('accepted'),
        }, function(data) {
            li.removeClass('loading')
                .data('accepted', data)
                .attr('data-accepted', data);
        });
    }

    $(function() {

        $(".proposals span.btn").click(function(event) {
            event.preventDefault();
            var li = $(this).closest('li');
            toggleProposal(li);
            return false;
        });
    });

});
