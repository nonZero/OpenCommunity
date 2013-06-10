$(function() {

    // Add invitation form
    $('#invite-form').ajaxForm(function(data) {
        var el = $(data.trim());
        $("#invite-form").closest('li').before(el).parent().listview('refresh');
        el.hide().show('slow');
        el.find('button').button();
        $("#invite-form").get(0).reset();
    });

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