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

        $('#add-comment').ajaxForm(function(data) {
            var el = $(data.trim());
            $("#add-comment").closest('li').before(el).parent().listview('refresh');
            el.find('button').buttonMarkup();
            $("#add-comment").get(0).reset();
        });

        $('#comments').on('click', '.delete-comment button', function() {
            var btn = $(this);
            var form = btn.closest('form');
            console.log(btn, form);
            var extra = {};
            if (btn.attr('name')) {
                extra[btn.attr('name')] = btn.attr('value');
            }
            form.ajaxSubmit({
                                data: extra,
                                success: function(data) {
                                    console.log(data, form);
                                    form.closest('li').toggleClass('deleted', data=='0');
                                }
                            });
            return false;
        });
    })


});
