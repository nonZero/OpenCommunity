"use strict";

$(function() {
   $('.issues li').click(function() {
       var li = $(this);
       $.post('', {
           issue: li.data('issue'),
           set: li.data('set')
           }, function(data) {
               console.log(li);
               li.data('set', data).attr('data-set', data);
               console.log(li.data('set'));
           });
   }) 
});
