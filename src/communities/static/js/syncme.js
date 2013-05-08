;(function ( $, window, document, undefined ) {

    "use strict";

    var pluginName = "syncMe",
        defaults = {
            prefix: "syncme_"
        };

    function SyncMe( element, options ) {
        this.element = element;

        this.options = $.extend( {}, defaults, options );

        this._defaults = defaults;
        this._name = pluginName;

        this.init();
    }

    SyncMe.prototype = {

        init: function() {

            var prefix = this.options.prefix;
            $(this.element).each(function() { 
                var el = $(this);
                var key = prefix + $(this).prop('id');
                if (localStorage[key] === undefined) {
                    localStorage[key] = el.val();
                } else {
                    el.val(localStorage[key]);
                }
                $(this).bind('input', function() {
                    localStorage[key] = el.val();
                })
                $(window).bind('storage', function(e) {
                    if (e.originalEvent.key == key) {
                        el.val(e.originalEvent.newValue);
                    }
                });
            });

        },

        foo: function(el) {
        }
    };

    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName, new SyncMe( this, options ));
            }
        });
    };

})( jQuery, window, document );