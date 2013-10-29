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
            $(this).find('.htmlarea textarea').each(function() {
                //$(this).tinymce().remove();
            });
            $(this).removeData('bs.modal').empty();
        });


        return false;
    });
});

// function wysiwygize(x) {
// 
    // x.tinymce({
        // script_url : tmce_url,
        // directionality : 'rtl',
        // language : 'he_IL',
        // menubar : false,
        // toolbar_items_size : 'small',
        // content_css : "/static/m/tinymce.css",
        // toolbar : "numlist bullist | alignjustify alignright aligncenter alignleft | underline italic bold",
    // });
// }

function initForm(modal) {

    var url = modal.data('bs.modal').options.remote;

    var form = modal.find('form');

    form.ajaxForm({

        url : url,

        beforeSubmit : function() {
            form.find('input[type="submit"]').prop('disabled', true);
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

//
// $.fn["html5inputs"] = function() {
// return this.each(function() {
// $(this).find('.dateinput').attr('type','date');
// $(this).find('.timeinput').attr('type','time');
// $(this).find('.datetimeinput').attr('type','datetime-local');
// $(this).find('.crequired input,.crequired select,.crequired textarea').attr('required','required');
// });
// };

