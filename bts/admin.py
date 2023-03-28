from django.contrib import admin

from .models import (AssortmentBox, Category, Component, ComponentType, SubComponent, Inventory,
                     Merchant, Purchase, PurchaseLine, StorageUnit,
                     StorageUnitCompartment, StorageUnitType)

from django.forms.widgets import Select
from django import forms


class MultiLevelSelect(Select):

    def __init__(self):
        super().__init__()
        self.template_name = "bts/multilevelselect/select.html"


class SubComponentAdmin(admin.ModelAdmin):
    search_fields = ["name", "component_type"]


class InventoryAdminForm(forms.ModelForm):

    storage_unit_compartment = MultiLevelSelect()

    class Meta:
        fields = ["sub_component",
                  "storage_unit_compartment", "timestamp", "count"]
        model = Inventory
        widgets = {
            'storage_unit_compartment': MultiLevelSelect
        }


class InventoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ["sub_component"]
    form = InventoryAdminForm


# Register your models here.
admin.site.register(AssortmentBox)
admin.site.register(Category)
admin.site.register(ComponentType)
admin.site.register(Component)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Merchant)
admin.site.register(Purchase)
admin.site.register(PurchaseLine)
admin.site.register(StorageUnit)
admin.site.register(StorageUnitCompartment)
admin.site.register(StorageUnitType)
admin.site.register(SubComponent, SubComponentAdmin)
