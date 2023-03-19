from django.contrib import admin

from .models import (AssortmentBox, Category, DigiKeyComponent, Inventory,
                     Merchant, Purchase, PurchaseLine, StorageUnit,
                     StorageUnitCompartment, StorageUnitType)

# Register your models here.
admin.site.register(AssortmentBox)
admin.site.register(Category)
admin.site.register(DigiKeyComponent)
admin.site.register(Inventory)
admin.site.register(Merchant)
admin.site.register(Purchase)
admin.site.register(PurchaseLine)
admin.site.register(StorageUnit)
admin.site.register(StorageUnitCompartment)
admin.site.register(StorageUnitType)
