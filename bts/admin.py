# Bauteilsortiment - An Electronic Component Archival System
# Copyright (C) 2023  nomike
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin

from .models import (AssortmentBox, Category, Component, ComponentType, SubComponent, Inventory,
                     Merchant, Purchase, PurchaseLine, StorageUnit,
                     StorageUnitCompartment, StorageUnitType)

from django.forms.widgets import Select
from django import forms


class MultiLevelSelect(Select):

    def __init__(self, fields):
        self.fields = fields
        super().__init__()
        self.template_name = "bts/multilevelselect/select.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['fields'] = self.fields
        return context


class SubComponentAdmin(admin.ModelAdmin):
    search_fields = ["name", "component_type__name"]
    autocomplete_fields = ["component", "component_type"]
    save_as = True


class ComponentAdmin(admin.ModelAdmin):
    search_fields = ['part_number', 'product_description']


class ComponentTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class InventoryAdminForm(forms.ModelForm):
    autocomplete_fields = ["sub_component"]

    class Meta:
        fields = ["sub_component",
                  "storage_unit_compartment", "timestamp", "count"]
        model = Inventory
        widgets = {
            'storage_unit_compartment': MultiLevelSelect(fields="""[
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
]""")
        }


class InventoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ["sub_component"]
    form = InventoryAdminForm


# Register your models here.
admin.site.register(AssortmentBox)
admin.site.register(Category)
admin.site.register(ComponentType, ComponentTypeAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Merchant)
admin.site.register(Purchase)
admin.site.register(PurchaseLine)
admin.site.register(StorageUnit)
admin.site.register(StorageUnitCompartment)
admin.site.register(StorageUnitType)
admin.site.register(SubComponent, SubComponentAdmin)
