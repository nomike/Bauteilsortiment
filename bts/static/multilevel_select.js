/*
Bauteilsortiment - An Electronic Component Archival System
Copyright (C) 2023  nomike

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
*/
django.jQuery(document).ready(function () {
    // Create the selects
    for (let i = 0; i < fields.length; i++) {
        django.jQuery("#" + widget_name).append(django.jQuery("<select>", { style: "width: 300px;", class: fields[i]['id'], name: i == fields.length - 1 ? widget_name : null }));
    }

    // Initialize select2
    for (let i = 0; i < fields.length; i++) {
        // django.jQuery('.' + fields[i]['id']).select2();
    }

    // Fill the first select, but don't select anything.
    fill_select(0);
    // Set the field value
    set_field(fields.length - 1, widget_value);

    for (let i = 0; i < fields.length; i++) {
        django.jQuery('.' + fields[i]['id']).change(
            function (event) {
                handle_change(i);
            }
        );
    }
});

/**
 * Clears all values from a select formfield.
 * @param {Number} select_id The index of the select
 */
function clear_select(select_id) {
    django.jQuery('.' + fields[select_id]['id']).empty();
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
    const select = django.jQuery('.' + fields[select_id]['id']);
    const model = fields[select_id]['model'];
    const display_field = fields[select_id]['display_field'];
    const parent_field = fields[select_id]['parent_field'];
    const id = select_id > 0 ? django.jQuery('.' + fields[select_id - 1]['id']).val() : null;

    let url;
    if (parent_field != null) {
        url = '/bts/api/v0/' + model + '/?' + parent_field + '=' + id;
    } else {
        url = '/bts/api/v0/' + model + '/';
    }
    console.info(url);
    django.jQuery.ajax({
        url: url,
        dataType: 'json',
        async: false,
        success: function (data) {
            let count = 0;
            django.jQuery.each(data['results'], function () {
                select.append(django.jQuery("<option />").val(this.id).text(this[display_field]));
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
        django.jQuery.ajax({
            url: `/bts/api/v0/${fields[i]['model']}/${selected_objects[i]}`,
            dataType: 'json',
            async: false,
            success: function (data) {
                django.jQuery.ajax({
                    url: data[fields[i]['parent_field']],
                    dataType: 'json',
                    async: false,
                    success: function (data2) {
                        selected_objects[i - 1] = data2['id'];
                    }
                });
            }
        });
    }
    for (let i = 0; i <= select_id; i++) {
        fill_select(i);
        django.jQuery('.' + fields[i]['id']).val(selected_objects[i]).change();
    }
}
