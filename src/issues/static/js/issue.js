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

        $(".proposals.open span.btn").click(function(event) {
            event.preventDefault();
            var li = $(this).closest('li');
            toggleProposal(li);
            return false;
        });
    });

    // Comments

    $(function() {
        $('#id_content').attr('required', 'required');
        $('#add-comment').ajaxForm(function(data) {
            $("#add-comment").closest('li').before($(data.trim())).parent().listview('refresh');
            $("#add-comment").get(0).reset();
        });
    })


});
