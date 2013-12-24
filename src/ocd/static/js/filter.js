"use strict";

/**
 * Toggles visibilty for titles with no "child" elements.
 */
function toggleTitles() {
    $('.filter-title').each(function() {
        $(this).toggle($(this).next().find('.filter:visible').length > 0);
    });
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

        toggleTitles();

    });

    toggleTitles();
});
