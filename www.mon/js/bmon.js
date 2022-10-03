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
            };

            that.onmessage = function (data) {
            };

            if(populate(that)) {
                Object.entries(that.modules).forEach(([k,v]) => {
                    v.fill_test();
                });
                return that;
            } else {
                throw 'Failed to create Bubble Monitor';
            }
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
        return true;
    }

    $.fn.bmon.module.logmodule =
        function (node, args) {
            var that = {};
            that.node = node;
            that.keys = args.split(',');

            // public API
            that.apply = function (data) {
                for(const item of data) {
                    let row = that.node.append("<tr></tr>")
                    for(const key of that.keys) {
                        row.append(`<td>${item[key]}</td>`)
                    }
                }
            };

            that.fill_test = function () {
                let dummy_data = [{
                    'col1': 'data_col1',
                    'col2': 'data_col2',
                    'col3': 'data_col3'
                }];
                that.apply(dummy_data);
            };

            return that;
        };

})(jQuery);
