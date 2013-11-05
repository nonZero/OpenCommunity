"use strict";

$(function() {

    $("body").on('click', 'a', function() {

        if ($(this).data('rel') != 'form') {
            return;
        }

        var url = $(this).attr('href');

        $('#modal-form').modal({
            remote : url
        }).one('hidden.bs.modal', function() {
            $(this).removeData('bs.modal').empty();
        });

        return false;
    });

});

function initForm(modal) {

    var url = modal.data('bs.modal').options.remote;

    var form = modal.find('form');
    form.find('.htmlarea textarea').wysihtml5({locale: "he-IL"});

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
