"use strict";

$(function() {
    $('#proposal-form button').click(function () {
        console.log($(this).val());
        $('#proposal-form').ajaxForm({
            data: {accepted: $(this).val()},
            success: function(resp) {
                history.back();
            }
        });
    });
});
