"use strict";

function refreshProposalForm() {

    // prevent html5 required field
    $('#id_proposal-title').prop('disabled', $('#id_proposal-type').val() == '');

    // hide task related fields
    var els = $('#id_proposal-title').parent().parent();
    var els1 = $('#id_proposal-content').parent().parent().parent().parent();
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

/* use tabs instead of drop down for proposal type */
function init_proposal_tabs(with_issue) {
    var TYPE_NONE = 0;
    var TYPE_TASK = 1;
    var TYPE_RULE = 2;
    var TYPE_ADMIN = 3;
    
    var IDX_NONE = 0;
    var IDX_ADMIN = 1;
    var IDX_RULE = 2;
    var IDX_TASK = 3;
    
    $("ul#proposal-type li").on('click', function() {
        $(this).addClass('active').siblings().removeClass('active');
        var type_select = $('#id_proposal-type')
        var proposal_controls = $('#id_proposal-content,#id_proposal-title').closest('.form-group');
        var task_controls = $('#id_proposal-assigned_to,#id_proposal-due_by').closest('.form-group');

        var selected_idx = $(this).index();
        if(!with_issue) {
            selected_idx += 1;
        }
        if (selected_idx == IDX_NONE) {
            type_select.val('');
            proposal_controls.hide();
            task_controls.hide();
            $("[id^='id_proposal']").prop('required', false);
        }
        else {
            proposal_controls.show();
            if (selected_idx == IDX_ADMIN) {
                type_select.val(TYPE_ADMIN);
                task_controls.hide();
            }
            else if (selected_idx == IDX_RULE) {
                type_select.val(TYPE_RULE);
                task_controls.hide();
            }
            else if (selected_idx == IDX_TASK) {
                type_select.val(TYPE_TASK);
                task_controls.show();
            }
            proposal_controls.prop('required', true);
        }
    });
}

function init_user_autocomplete(ac_url) {
    //{% verbatim %}
    var tpl = '<p>{{#board}}<strong>{{/board}}{{user__display_name}}{{#board}}</strong>{{/board}}</p>'
    var tpl1 = '<p><strong>-- {{value}} --</strong></p>'
    //{% endverbatim %}
    $("[id$='assigned_to']").typeahead({
        remote: ac_url + '?q=%QUERY',
        valueKey: 'user__display_name',
        engine: Hogan,
        template: tpl
    }).css('background-color', '#fff');
}

function searchIssues(term) {
	$(".issue-table tr").each(function() {
		$(this).toggle(!term || $(this).text().indexOf(term) > 0);
	});
}
