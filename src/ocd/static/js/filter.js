/* ========================================================================
 * Filter: filter.js v0.1
 * ======================================================================== */

+ function($) {"use strict";

    // Filter PUBLIC CLASS DEFINITION
    // ================================

    var Filter = function(element, options) {
        this.$element = $(element);
        this.options = $.extend({}, Filter.DEFAULTS, options);
    };

    Filter.DEFAULTS = {
    };

    Filter.prototype.activate = function() {
        this.$element.closest('ul').children('li').removeClass('active');
        this.$element.parent('li').addClass('active');
        if (this.options.hide) {
            $(this.options.hide).hide().removeClass('on');
        }
        if (this.options.show) {
            $(this.options.show).show().addClass('on');
        }
        $('.filter-title').each(function() {
            $(this).toggle(
                $(this).next().find('.filter:visible').length > 0
            );
        });
    };

    // FILTER PLUGIN DEFINITION
    // ==========================

    var old = $.fn.filter;

    $.fn.filter = function(option) {
        return this.each(function() {
            var $this = $(this);
            var data = $this.data('oc.filter');
            var options = $.extend({}, Filter.DEFAULTS, $this.data(), typeof option == 'object' && option);

            if (!data) {
                $this.data('oc.filter', ( data = new Filter(this, options)));
            }
            data[typeof option == 'string' ? option : 'activate']();
        });
    };

    $.fn.filter.Constructor = Filter;

    // COLLAPSE NO CONFLICT
    // ====================

    $.fn.filter.noConflict = function() {
        $.fn.filter = old;
        return this;
    };

    // COLLAPSE DATA-API
    // =================

    $(document).on('click.filter.data-api', '[data-toggle=filter]', function(e) {
        var $this = $(this);
        var data = $this.data('oc.filter');
        var options = data ? 'activate' : $this.data();
        $this.filter(options);
        return false;
    });

}(window.jQuery);
