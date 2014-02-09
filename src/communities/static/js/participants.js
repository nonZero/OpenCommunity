
$(function() {
    $('.participant-title button').on('click', function() {
        $(".select-participants, .list-of-participants").toggle();
        $(".participants-body-list, .participants-body-form").toggle();
    });
  
    $('.board_select').on('change', 'li input', function() {
       var uid = $(this).val();
       var sel = $(this).is(':checked');
       $('#p_select input[value="' + uid + '"]').prop('checked', sel);
    })
    
    // user autocomplete setup
    var tpl = '<p>{{value}}</p>';
    var member_tpl = '<li class="list-group-item" data-uid="#ID#">' +
					           '<div style="display: inline;line-height: 30px;">' +
					           '#NAME#</div>' +
					           '<button class="del_member pull-right btn btn-danger btn-sm">' +
						         '<i class="fa fa-trash-o"></i> {% trans "Delete" %}' +
					           '</button></li>';
                   var guest_tpl = 	'<li class="list-group-item" data-guest="#GUEST_RAW#">' +
                      '<div style="display: inline;line-height: 30px;">' + 
						          '#G_DETAIL#</div>' + 
					            '<button class="pull-right btn btn-danger btn-sm">' +
                      '<i class="fa fa-trash-o"></i> {% trans "Delete" %}</button></li>';

    $("#add_member").typeahead({
      prefetch : typeahead_url,
        cache: false,
        remote : typeahead_url + '?q=%QUERY',
        engine : Hogan,
        // template : tpl
    }).css('background-color', '#fff');

   $("#add_member").on('typeahead:selected', function (object, datum) {
     console.log($(this).val());
     $(this).data('uid', datum['user__id']);
   });

   $('#members').on('click', '#add_member_btn', function() {     
      var uid = $('#add_member').data('uid'); 
      $('#p_select input[value="' + uid + '"]').prop('checked', true);
      var mem_list = $('ul#members-list');
      var new_name = $('#add_member').val();
      if(new_name && uid) {
          mem_list.append($(member_tpl.replace('#NAME#', new_name).replace('#ID#', uid)));
      }
      $('#add_member').data('uid', '').val('');

    })
    
    $('#members').on('click', 'button.del_member', function(ev) { 
        ev.preventDefault();
        alert($(this).closest('li').data('uid'));
        return (true);
    });

   $('#guests').on('click', '#add_guest_btn', function() {     
      var guest_name_inp = $('input#guest_name');
      var guest_email_inp = $('input#guest_email');
      
      // validate name
      if(guest_name_inp.val() == '') {
          guest_name_inp.focus().css('border-color', 'red');
          return;  
      }
      else {
          guest_name_inp.css('border-color', '#ccc');  
      }
      // validate guests fields
      if( ! guest_email_inp.get(0).checkValidity() ) {
          guest_email_inp.focus().css('border-color', 'red');
          return;
      }
      else {
          guest_email_inp.css('border-color', '#ccc');  
      }

      var guest_details = guest_name_inp.val();
      if(guest_email_inp.val()) {
          guest_details += ' [' + guest_email_inp.val() + ']';
      }
      $('ul#guests-list').append($(guest_tpl.replace('#G_DETAIL#', guest_details)));
      var cur_guests = $('#id_upcoming_meeting_guests').val();
      $('#id_upcoming_meeting_guests').val(cur_guests + '\n' + guest_details);
      $('#guests input').val('');
      
    });
}); 
