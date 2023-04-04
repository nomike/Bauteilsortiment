const fields = [
    {
        'id': '.select-assortment-box',
        'model': 'AssortmentBox',
        'display_field': 'name',
    },
    {
        'id': '.select-storage-unit',
        'model': 'StorageUnit',
        'display_field': 'number',
        'parent_field': 'assortment_box_id'
    },
    {
        'id': '.select-storage-unit-compartment',
        'model': 'StorageUnitCompartment',
        'display_field': 'name',
        'parent_field': 'storage_unit_id'
    }
]


$(document).ready(function () {
    // Initialize select2
    for (let i = 0; i < fields.length; i++) {
        $(fields[i]['id']).select2();
    }

    // Fill the first select, but don't select anything.
    fill_select(0);
});

function clear_select(select_id) {
    console.debug(`clear_select(${select_id})`);
    $(fields[select_id]['id']).empty();
}


function handle_change(select_id) {
    console.debug(`Handling change event for select_id=${select_id} (value=${$(fields[select_id]['id']).val()})`);

    const select_number = select_id + 1;
    for (let i = select_number; i < fields.length; i++) {
        console.debug(`Emptying select ${fields[i]['id']}`);
        clear_select(i);
    }
    if (select_number < fields.length) {
        console.debug(`Fill select ${select_number}`);
        fill_select(select_number);
    }
}

function fill_select(select_id) {
    clear_select(select_id);
    const select = $(fields[select_id]['id']);
    const model = fields[select_id]['model'];
    const display_field = fields[select_id]['display_field'];
    const filter_model = select_id > 0 ? fields[select_id - 1]['model'] : null;
    const id = select_id > 0 ? $(fields[select_id - 1]['id']).val() : null;

    console.debug(`fill_select(select_id=${select_id}); // select=${select}, model=${model}, display_field=${display_field}, filter_model=${filter_model}, id=${id})`);
    let url;
    if (filter_model != null) {
        url = '/bts/json/' + model + '/' + filter_model + '/' + id;
    } else {
        url = '/bts/json/' + model;
    }
    console.debug(`URL=${url}`);

    $.ajax({
        url: url,
        dataType: 'json',
        async: false,
        success: function (data) {
            let count = 0;
            $.each(data, function () {
                console.debug(`###COUNT=${count++}`);
                console.debug(`Appending option ${this[display_field]} to select {select_id}`);
                select.append($("<option />").val(this.id).text(this[display_field]));
                console.debug("Done getting JSON");
                log_list_value(select_id, `done`);
            });
        }
    });
    handle_change(select_id);
}


function log_list_value(id, text = "foo") {
    console.debug(`${text}: Value of list ${id} is ${$(fields[0]['id']).val()}`);
}

function set_field(field_id, value) {
    let selected_objects = [];
    selected_objects[field_id] = value;

    for (let i = field_id; i > 0; i--) {
        $.ajax({
            url: `/bts/json/${fields[i]['model']}/${selected_objects[i]}/field/${fields[i]['parent_field']}`,
            dataType: 'json',
            async: false,
            success: function (data) {
                selected_objects[i - 1] = data;
            }
        });
    }

    for (let i = 0; i < field_id; i++) {
        console.error(`>>>i=${i}`);
        fill_select(i);
        $(fields[i]['id']).val(selected_objects[i]).change();
    }

    console.debug(`## selected_objects=${selected_objects}`);
} 
