(function ($) {

    // create the robomind namespace 'rm'
    $.fn.bmon = {};
    $.fn.bmon.module = {};

    var defaults = {
        aap: 'noot'
    };

    $.fn.bmon.bubble_monitor =
        function (node, modules) {
            var that = {};
            for (n in defaults) {
                that[n] = defaults[n];
            }
            that.node = node;
            that.moduledefs = modules;
            that.modules = {};

            that.timer = function () {
                console.log("eikel");
            };

            that.onmessage = function (data) {
            };

            populate(that)

            return that;
        };

    function populate(that) {
        // find modules to manage
        Object.entries(that.moduledefs).forEach(([mname, mtype]) => {
            let classname = `.${mname}`;
            that.node.find(classname).each(function (ix) {
                let node = $(this);
                let args = node.attr("data-module");
                console.log(args);
                that.modules[node.attr('id')] = mtype(node, args);
            });

        })
    }

    $.fn.bmon.module.logmodule =
        function (node, args) {
            var that = {};
            that.node = node;
            that.args = args;

            // public API
            that.apply = function (data) {
            };

            return that;
        };

})(jQuery);
