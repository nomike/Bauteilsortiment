const fields = [
    {
        'id': 'select-assortment-box',
        'model': 'AssortmentBox',
        'display_field': 'name',
    },
    {
        'id': 'select-storage-unit',
        'model': 'StorageUnit',
        'display_field': 'number',
        'parent_field': 'assortment_box_id'
    },
    {
        'id': 'select-storage-unit-compartment',
        'model': 'StorageUnitCompartment',
        'display_field': 'name',
        'parent_field': 'storage_unit_id'
    }
]


$(document).ready(function () {
    for (let i = 0; i < fields.length; i++) {
        $("#select_test > formfields").append($("<select>", { style: "width: 300px;", class: fields[i]['id'] }));
    }

    // Initialize select2
    for (let i = 0; i < fields.length; i++) {
        $('.' + fields[i]['id']).select2();
    }

    // Fill the first select, but don't select anything.
    fill_select(0);
});

/**
 * Clears all values from a select formfield.
 * @param {Number} select_id The index of the select
 */
function clear_select(select_id) {
    $('.' + fields[select_id]['id']).empty();
}

/**
 * Callback for handling a value change of a select.
 * It clears all selects to the right and fills them with new values.
 * @param {Number} select_id The index of the select
 */
function handle_change(select_id) {
    const select_number = select_id + 1;
    for (let i = select_number; i < fields.length; i++) {
        clear_select(i);
    }
    if (select_number < fields.length) {
        fill_select(select_number);
    }
}

/**
 * Fill a select with values. If it is not the left most select, it will use the current value from the previous select as a filter.
 * @param {Number} select_id The index of the select
 */
function fill_select(select_id) {
    clear_select(select_id);
    const select = $('.' + fields[select_id]['id']);
    const model = fields[select_id]['model'];
    const display_field = fields[select_id]['display_field'];
    const filter_model = select_id > 0 ? fields[select_id - 1]['model'] : null;
    const id = select_id > 0 ? $('.' + fields[select_id - 1]['id']).val() : null;

    let url;
    if (filter_model != null) {
        url = '/bts/json/' + model + '/' + filter_model + '/' + id;
    } else {
        url = '/bts/json/' + model;
    }

    $.ajax({
        url: url,
        dataType: 'json',
        async: false,
        success: function (data) {
            let count = 0;
            $.each(data, function () {
                select.append($("<option />").val(this.id).text(this[display_field]));
            });
        }
    });
    handle_change(select_id);
}

/**
 * Set the value of a select. This will set the values of the selects to the left to the appropriate values as well.
 * @param {Number} select_id The index of the select
 * @param {Number} value    The value you want to set the select to
 */
function set_field(select_id, value) {
    let selected_objects = [];
    selected_objects[select_id] = value;

    for (let i = select_id; i > 0; i--) {
        $.ajax({
            url: `/bts/json/${fields[i]['model']}/${selected_objects[i]}/field/${fields[i]['parent_field']}`,
            dataType: 'json',
            async: false,
            success: function (data) {
                selected_objects[i - 1] = data;
            }
        });
    }

    for (let i = 0; i < select_id; i++) {
        fill_select(i);
        $('.' + fields[i]['id']).val(selected_objects[i]).change();
    }
}
