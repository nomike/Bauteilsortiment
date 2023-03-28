from django.contrib import admin

from .models import (AssortmentBox, Category, Component, ComponentType, SubComponent, Inventory,
                     Merchant, Purchase, PurchaseLine, StorageUnit,
                     StorageUnitCompartment, StorageUnitType)


class SubComponentAdmin(admin.ModelAdmin):
    search_fields = ["name", "component_type"]


class InventoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ["sub_component"]


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
