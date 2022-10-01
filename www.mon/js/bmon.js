(function($) {

    // create the robomind namespace 'rm'
    $.fn.bmon = {};
    $.fn.bmon.module = {};

        var defaults = {
            aap: 'noot'
        };

        $.fn.bmon.bubble_monitor =
            function(node, modules) {
                var that = {};
                for (n in defaults) {
                    that[n] = defaults[n];
                }
                that.node = node;
                that.modules = modules;

                // public API
                that.start = function () {
                    doStart(that);
                };

                that.timer = function () {
                };

                that.onmessage = function (data) {
                };

                populate(that)

                return that;
            };

        function populate(that) {
            Object.entries(that.modules).forEach(([mname,mtype]) => {
                let classname = `.${mname}`;
                that.node.find(classname).each(function(ix) {
                    console.log($(this).attr('id'));
                });

            })
        }

        function doStart(that) {
        }

    $.fn.bmon.module.logmodule =
        function() {
            var that = {};
            for (n in defaults) {
                that[n] = defaults[n];
            }

            // public API
            that.start = function () {
            };

            return that;
        };

})(jQuery);
