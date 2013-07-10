"use strict";

$(function() {


    $("body").on('click', 'a', function() {

        if ($(this).data('rel') != 'form') {
            return;
        }

        var url = $(this).attr('href');

        $.get(url, function(resp) {
            var p = $(resp.trim()).html5inputs().appendTo("#mypopups")
                .popup({dismissible: false})
                .trigger('create')
                .popup('open')
                .on("popupafterclose", function(event, ui) {
                    $(this).popup('destroy');
                    p.find('textarea.wysiwyg').each(function() {
                        $(this).tinymce().remove();
                    });
                    p.detach();
                 });

            p.find('textarea.wysiwyg').tinymce({
                   directionality : 'rtl',
                   language : 'he_IL',
                   menubar: false,
                   toolbar_items_size: 'small',
                   toolbar: "bold italic underline | bullist numlist | blockquote",
            });

            var form = p.find('form');

            form.ajaxForm({

                url: url,

                beforeSubmit: function() {
                    form.find('input[type="submit"]').prop('disabled', true);
                },

                success: function(resp) {
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

                error: function(resp) {
                    if (resp.status == 403) {
                        var newEl = $(resp.responseText.trim()).html5inputs();
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
});

$.fn["html5inputs"] = function() {
    return this.each(function() {
        $(this).find('.dateinput').attr('type','date');
        $(this).find('.timeinput').attr('type','time');
        $(this).find('.datetimeinput').attr('type','datetime-local');
        $(this).find('.crequired input,.crequired select,.crequired textarea').attr('required','required');
    });
};
