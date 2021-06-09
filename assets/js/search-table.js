(function ($) {
    'use strict';

    function delay(callback, ms) {
        var timer = 0;
        return function () {
            var context = this,
                args = arguments;
            clearTimeout(timer);
            timer = setTimeout(function () {
                callback.apply(context, args);
            }, ms || 0);
        };
    }


    function setUpOptions(options) {
        const placeholderConst = "Enter a search term";
        var defaultOptions = options || {
            placeholder: placeholderConst,
            filterTrClass: ""
        };
        if (defaultOptions.placeholder === undefined)
            defaultOptions.placeholder = placeholderConst;
        if (defaultOptions.filterTrClass === undefined)
            defaultOptions.filterTrClass = "";
        return defaultOptions;
    }
    var searchTable = function (table, options) {
        this.setUp = function () {
            var defaultOptions = setUpOptions(options);
            var inputSearch = $("<input>", {
                type: "text",
                'class': "form-control shadow-none",
                placeholder: defaultOptions.placeholder
            });
            var spanSearch = $("<span>", {
                'class': "add-on"
            }).append($("<i>", {
                'class': "icon icon-search"
            }))
            var divSearch = $("<div>", {
                'class': "row-fluid input-append"
            });
            divSearch.append(inputSearch).append(spanSearch);
            $(table).before(divSearch);
            var $rows = $(table).find('tbody tr' + defaultOptions.filterTrClass);

            inputSearch.keyup(delay(function (e) {
                if (typeof defaultOptions.before === 'function')
                    defaultOptions.before();
                var val = '^(?=.*' + $.trim($(this).val()).split(/\s+/).join(')(?=.*') + ').*$',
                    reg = RegExp(val, 'i'),
                    text;
                $rows.show().filter(function () {
                    text = $(this).text().replace(/\s+/g, ' ');
                    return !reg.test(text);
                }).hide();
            }, 500));
        }
    }
    $.fn.searchTable = function (options) {
        var st = new searchTable(this, options);
        st.setUp();
    }
})(jQuery);