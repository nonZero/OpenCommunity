"use strict";

function refreshProposalForm() {

    // prevent html5 required field
    $('#id_proposal-title').prop('disabled', $('#id_proposal-type').val() == '');

    // hide task related fields
    var els = $('#div_id_proposal-title,#div_id_proposal-content');
    if ($('#id_proposal-type').val() == '') {
        els.hide();
    } else {
        els.show();
    }

    // hide task related fields
    var els = $('#div_id_proposal-assigned_to,#div_id_proposal-due_by');
    if ($('#id_proposal-type').val() == '1') {
        els.show();
    } else {
        els.hide();
    }

}

$(function() {
    $('body').on('change', '#id_proposal-type', refreshProposalForm )
});
