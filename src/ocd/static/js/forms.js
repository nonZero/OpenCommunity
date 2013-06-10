"use strict";

$(function() {

    $('body').on('pagebeforechange', function(event, data) {

        if (data.options['role'] != 'dialog') {
            return;
        }

        if (data.toPage.dialog) {
            var el = data.toPage;
            el.dialog( "option", "closeBtn", "none" );
            el.find('.ui-header a').click(function() {
                el.dialog("close");
                return false;
            });
            var form = data.toPage.find('form');
            form.ajaxForm({
                url: data.absUrl,
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
        }
    });

    $("body").on('click', 'a', function() {

        if ($(this).data('rel') != 'form') {
            return;
        }

        $.mobile.changePage($(this).attr('href'), {
            role: "dialog",
            changeHash: false
        });

        return false;
    });
})


