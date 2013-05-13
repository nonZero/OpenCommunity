"use strict";

$(function () {

    function toggleProposal(el) {
        el.addClass('loading');
        $.post('', {
            issue : el.data('id'),
            accepted : el.data('accepted'),
        }, function(data) {
            el.removeClass('loading')
                .data('accepted', data)
                .attr('data-accepted', data);
        });
    }

    $(function() {

        $(".accept,.unaccept").click(function(event) {
            event.preventDefault();
            var el = $(this).closest('.proposal');
            toggleProposal(el);
            return false;
        });
    });


})
