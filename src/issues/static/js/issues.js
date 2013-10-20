"use strict";

function refreshProposalForm() {

    // prevent html5 required field
    $('#id_title').prop('disabled', $('#id_type').val() == '');

    // hide task related fields
    var els = $('#div_id_title,#div_id_content');
    if ($('#id_type').val() == '') {
        els.hide();
    } else {
        els.show();
    }

    // hide task related fields
    var els = $('#div_id_assigned_to,#div_id_due_by');
    if ($('#id_type').val() == '1') {
        els.show();
    } else {
        els.hide();
    }

}

$(function() {
    $('body').on('change', '#id_type', refreshProposalForm )
});
