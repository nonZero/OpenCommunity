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

    $(".proposals.open span.btn").click(function(event) {
        event.preventDefault();
        var li = $(this).closest('li');
        toggleProposal(li);
        return false;
    });

    // Comments

    // Add comment form
    $('#add-comment').ajaxForm(function(data) {
        var el = $(data.trim());
        $("#add-comment").closest('li').before(el).parent().listview('refresh');
        el.find('button').button();
        $("#add-comment").get(0).reset();
    });

    // Delete and undelete comment form
    $('#comments').on('click', '.delete-comment button', function() {
        var btn = $(this);
        var form = btn.closest('form');
        var extra = {};
        if (btn.attr('name')) {
            extra[btn.attr('name')] = btn.attr('value');
        }
        form.ajaxSubmit({
                            data: extra,
                            success: function(data) {
                                form.closest('li').toggleClass('deleted', data=='0');
                            }
                        });
        return false;
    });

    // Edit comment Form:

    //  - start edit
    $('#comments').on('click', '.edit-comment button', function() {
        var btn = $(this);
        var li = btn.closest('li'); 
        li.addClass('editing');
        var el = $("<div>Loading...</div>");
        li.find('.comment-inner').hide().after(el);
        $.get(btn.data('url'), function(data) {
            el.html(data).find('button').button();
        })
    });

    // - cancel edit
    $('#comments').on('click', '.cancel-edit-comment button', function() {
        var btn = $(this);
        var li = btn.closest('li'); 
        li.removeClass('editing');
        li.find('.comment-inner').show();
        li.find('.edit-issue-form').parent().remove();
    });

    // - save edits
    $('#comments').on('click', '.save-comment button', function() {
        var btn = $(this);
        btn.button('disable');
        var form = btn.closest('form');
        form.ajaxSubmit(function(data) {
                            if (!data) {
                                btn.button('enable');
                                return;
                            }
                            var new_li = $(data.trim());
                            new_li.find('button').button();
                            new_li.find('textarea').attr('required', 'required');
                            form.closest('li').replaceWith(new_li);
                            $("#comments").listview('refresh');
                        });
        return false;
    });

});
