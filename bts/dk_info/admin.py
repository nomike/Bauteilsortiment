from django.contrib import admin

from .models import (AssortmentBox, Category, DigiKeyComponent, ComponentType, SubComponent, Inventory,
                     Merchant, Purchase, PurchaseLine, StorageUnit,
                     StorageUnitCompartment, StorageUnitType)

# Register your models here.
admin.site.register(AssortmentBox)
admin.site.register(Category)
admin.site.register(ComponentType)
admin.site.register(DigiKeyComponent)
admin.site.register(Inventory)
admin.site.register(Merchant)
admin.site.register(Purchase)
admin.site.register(PurchaseLine)
admin.site.register(StorageUnit)
admin.site.register(StorageUnitCompartment)
admin.site.register(StorageUnitType)
admin.site.register(SubComponent)
