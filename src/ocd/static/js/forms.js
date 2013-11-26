"use strict";

$(function() {

    $("body").on('click', 'a', function() {

        if ($(this).data('rel') != 'form') {
            return;
        }

        var url = $(this).attr('href');
        var modal = $('#modal-form');

        var origin = $(this);

        $.get(url, function(html) {
            modal.html(html);
            initForm(modal, url, origin);
            modal.modal({}).one('hidden.bs.modal', function() {
                $(this).removeData('bs.modal').empty();
            });
        }).fail(function() {
            alert('Server Error, pleae reload page.');
        });

        return false;
    });

    if (navigator.userAgent.match('CriOS')) {
        $('body').addClass('ios-chrome');
    }

});

/**
 * Initializes an ajax form to allow refreshing on error and redirecting,
 * reloading, going back or calling a custom callback function on success.
 *
 * @param {jQuery} modal
 * @param {jQuery} origin optional. The original link clicked to
 */
function initForm(modal, url, origin) {

    var form = modal.find('form');

    form.find('.htmlarea textarea').wysihtml5({
        locale : "he-IL"
    }).css({
        'width' : '100%',
        'border-top-right-radius' : '0',
        'border-top-left-radius' : '0',
        'border-top' : '0'
    }); 

    form.ajaxForm({

        url : url,

        beforeSubmit : function() {
            form.find('input[type="submit"]').prop('disabled', true);
            if (form.find('input[type="file"]').length > 0) {
                $('input#id_file').parent().find('span.loader').remove();
                $('input#id_file').parent().append($('span.loader:first').clone().show());
            }
        },

        success : function(resp) {
            if (resp) {

                var appendTo = $(origin).data('append-to');
                if (appendTo) {
                    $(appendTo).append(resp);
                    $(modal).modal('hide');
                    return;
                }

                if (resp == '-') {
                    window.history.back();
                } else {
                    window.location.href = resp;
                }
            } else {
                window.location.reload();
            }
        },

        error : function(resp) {
            if (resp.status == 403) {
                var newEl = $(resp.responseText.trim());
                form.html(newEl.find('form').html());
            } else {
                alert('Server Error! please try again or reload the page.');
                form.find('input[type="submit"]').prop('disabled', false);
            }
        }
    });

}
