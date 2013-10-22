"use strict";

function unacceptProposal(el) {
    $.post('', {
        issue : el.data('id'),
        accepted : el.data('accepted'),
        unaccept: '1',
    }, function(data) {
        history.back();
    });
}


$(function() {

    $(".unaccept").click(function(event) {
        event.preventDefault();
        var el = $(this).closest('.proposal');
        unacceptProposal(el);
        return false;
    });

});