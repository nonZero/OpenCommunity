"use strict";

/**
 * Toggles visibilty for titles with no "child" elements.
 */
function toggleTitles() {
    $('.filter-title').each(function() {
        $(this).toggle($(this).next().find('.filter:visible').length > 0);
    });
}

function setHeight() {
	var Issues = $('.issue_right_column').outerHeight();
	var Issue = $('.issue_left_column').outerHeight();
  // console.log('----------> ' + Issues + ' , ' + Issue)
	if (Issues > Issue) {
		$('.issue_left_column').outerHeight(Issues+20);
	};
}

$(function() {

    $(document).on('click.filter.data-api', '[data-toggle=filter]', function(e) {

        var $this = $(this);

        var root = $this.closest('[data-filter]');
        root.find('li').removeClass('active');
        $this.parent('li').addClass('active');
        $this.closest('li.dropdown').addClass('active');
        if ($this.data('show')) {
            $(root.data('filter')).hide().removeClass('on');
            $($this.data('show')).show().addClass('on');
        } else {
            $(root.data('filter')).show().addClass('on');
        }
        if ($this.data('hide')) {
            $($this.data('hide')).hide().removeClass('on');
        }

        toggleTitles();
        setHeight();

    });

    toggleTitles();
    setHeight();
});
