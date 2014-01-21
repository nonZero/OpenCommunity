"use strict";

$(function() {

    function do_members_vote(vote_url, vote_value, user_id, elem) {
        $.post(vote_url, {
            val : vote_value,
            user : user_id
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
        do_members_vote(target, vote_value, user_id, $(this));
    });

});
