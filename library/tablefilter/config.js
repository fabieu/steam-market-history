var filtersConfig = {
    base_path: 'libary/tablefilter/',
    auto_filter: {
        delay: 500 //milliseconds
    },
    col_0: 'none',
    col_1: 'select',
    col_types: [
        'string',
        'string',
        'string',
        'string',
        'formatted-number', // defaults to '.' for decimal and ',' for thousands
    ],
    highlight_keywords: true,
    responsive: true,
    filters_row_index: 1,
    no_results_message: true,
    state: true,
    alternate_rows: true,
    rows_counter: true,
    btn_reset: true,
    status_bar: true,
    // popup_filters: true,
    msg_filter: 'Filtering...'
};
var tf = new TableFilter('data', filtersConfig);
tf.init();

setTimeout(function (){
    document.getElementById("loader").style.display = "none";
    document.getElementById("data").style.display = "block";
}, 500);
