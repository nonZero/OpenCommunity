"use strict";

$(function() {


    $("body").on('click', 'a', function() {

        if ($(this).data('rel') != 'form') {
            return;
        }

        var url = $(this).attr('href');

        $.get(url, function(resp) {
            var p = $(resp.trim()).popup({dismissible: false}).trigger('create').popup('open');
            var form = p.find('form');

            form.ajaxForm({

                url: url,

                beforeSubmit: function() {
                    form.find('input[type="submit"]').prop('disabled', true);
                },

                success: function(resp) {
                    if (resp) {
                        window.location.href = resp;
                    } else {
                        window.location.reload();
                    }
                },

                error: function(resp) {
                    if (resp.status == 403) {
                        var newEl = $(resp.responseText.trim());
                        form.html(newEl.find('form').html()).trigger('create');
                    } else {
                        alert('Server Error! please try again or reload the page.');
                        form.find('input[type="submit"]').prop('disabled', false);
                    }
                }

            });

            p.find('.close-dialog').click(function(ev) {
                p.popup('close');
                return false;
            });


        });

        return false;
    });
})


