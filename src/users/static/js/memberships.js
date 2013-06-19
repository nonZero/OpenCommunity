$(function() {

    // Add invitation form
    $('#invite-form').ajaxForm({

        success: function(data) {
            var el = $(data.trim());
            $("#invite-form").closest('li').before(el).parent().listview('refresh');
            el.hide().show('slow');
            el.find('button').button();
            $("#invite-form #id_email").val("");
        },
        error: function(resp) {
                if (resp.status == 403) {
                    $("#popup-content").text(resp.responseText);
                    $("#popup").popup({dismissible: true}).popup('open');
                } else {
                    alert('Server Error! please try again or reload the page.');
                }
            }
        })


    // Delete invitation form
    $('#invitations').on('click', '.delete-invitation button', function() {
        var btn = $(this);
        var form = btn.closest('form');
        form.ajaxSubmit({
                            success: function(data) {
                                form.closest('li').hide('slow', function(){
                                    $(this).remove();
                                    $("#invitations").listview('refresh');
                                    });
                            }
                        });
        return false;
    });

});