"use strict";

/**
 * Toggles visibilty for titles with no "child" elements.
 */
function toggleTitles() {
    $('.filter-title').each(function () {
        $(this).toggle($(this).next().find('.filter:visible').length > 0);
    });
}

function setHeight() {
    var issues_h = $('.issue_right_column').outerHeight();
    var frame_h = $('.issue_left_column').outerHeight();
    var inner_h = $('.issue_left_column_inner').outerHeight();
    if ((inner_h > frame_h) || (issues_h > frame_h)) {
        $('.issue_left_column').outerHeight(Math.max(inner_h, issues_h) + 20);
    }
}

$(function () {

    $(document).on('click.filter.data-api', '[data-toggle=filter]', function (e) {

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
