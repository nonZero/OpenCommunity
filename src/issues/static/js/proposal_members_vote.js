"use strict";

$(function() {

    function do_members_vote(vote_url, vote_value, user_id) {
        $.post(vote_url, {
            val : vote_value,
            user : user_id,
            board: '1',
        }, function(data) {
            if (data['result'] == 'ok') {
                $('#member_vote_sum').html(data['sum']);
            }
        });
    }
    function all_members_vote(vote_url, vote_value, user_ids) {
        $.post(vote_url, {
            val : vote_value,
            users : JSON.stringify(user_ids)
        }, function(data) {
            if (data['result'] == 'ok') {
                $('#member_vote_sum').html(data['sum']);
            }
        });
    }

    $(".container").on("change", "input:radio", function(event) {
        var vote_value = $(this).val();
        var target = $(this).attr('data-href');
        var user_id = $(this).attr('name').substr(11);
        do_members_vote(target, vote_value, user_id);
    });


	$(".container").on("click", ".all-pro,.all-con,.all-neutral", function(event) {
		var vote_value = $(this).data('value');
		var target = $(this).data('href') + "multi/";
		var user_ids = $.map($('fieldset:not([disabled]) input[value="' + vote_value + '"]').prop("checked", "1"), function(obj) {
			return $(obj).attr('name').substr(11);
		});
		all_members_vote(target, vote_value, user_ids);
	}); 

});
