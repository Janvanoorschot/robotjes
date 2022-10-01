(function($) {

    // create the robomind namespace 'rm'
    $.fn.bmon = {};

        var defaults = {
            aap: 'noot'
        };

        $.fn.bmon.bubble_monitor =
            function() {
                var that = {};
                for (n in defaults) {
                    that[n] = defaults[n];
                }
                that.node = "node";

                // public API
                that.start = function () {
                    doStart(that);
                };

                that.timer = function () {
                    console.log("timer");
                };

                that.onmessage = function (data) {
                    console.log("onmessage");
                };

                return that;
            };

        // Private functions
        function doStart(that) {
        }

})(jQuery);
