"use strict";

function refreshProposalForm() {

    // prevent html5 required field
    $('#id_proposal-title').prop('disabled', $('#id_proposal-type').val() == '');

    // hide task related fields
    var els = $('#id_proposal-title').parent().parent();
    var els1 = $('#id_proposal-content').parent().parent().parent();
    if ($('#id_proposal-type').val() == '') {
        els.hide();
        els1.hide();
        $('#id_proposal-title,#id_proposal-type').removeAttr('required');
    } else {
        els.show();
        els1.show();
        $('#id_proposal-title,#id_proposal-type').prop('required',true);
    }

    // hide task related fields
    var els = $('#id_proposal-assigned_to,#id_proposal-due_by').parent().parent();
    if ($('#id_proposal-type').val() == '1') {
        els.show();
    } else {
        els.hide();
    }

}

function searchIssues(term) {
	$(".issue-table tr").each(function() {
		$(this).toggle(!term || $(this).text().indexOf(term) > 0);
	});
}

$(function() {
    $('body').on('change', '#id_proposal-type', refreshProposalForm);
    $('input.issue-search').bind('input', function() {
    	searchIssues($(this).val().trim());
    });
});
