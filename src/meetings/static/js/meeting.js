"use strict";

$(function() {
   $('.issues li').click(function() {
       var li = $(this).addClass('loading');
       $.post('', {
           issue: li.data('issue'),
           set: li.data('set')
           }, function(data) {
               li.data('set', data).attr('data-set', data).removeClass('loading');
           });
   })
});
