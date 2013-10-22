"use strict";

function unacceptProposal(id, value) {
    $.post('', {
        issue : id,
        accepted : value,
        unaccept: '1',
    }, function(data) {
        history.back();
    });
}


$(function() {

    $(".proposal-action").click(function(event) {
        event.preventDefault();
        var el = $(this).closest('.proposal');
        unacceptProposal(el.data('id'), $(this).val());
        return false;
    });

    $(".unaccept").click(function(event) {
        event.preventDefault();
        var el = $(this).closest('.proposal');
        unacceptProposal(el.data('id'), $(this).data('value'));
        return false;
    });


});

