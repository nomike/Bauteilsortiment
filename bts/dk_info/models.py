from django.db import models
from django.utils import timezone
import datetime
import os
import sys
import digikey
from digikey.v3.productinformation import KeywordSearchRequest
import datetime
# Create your models here.

os.environ['DIGIKEY_CLIENT_ID'] = 'i1DbG9gggftX71MLTUngzAayWRMUzMGO'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'piWwjB6V8TYsxlLg'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = './cache'


class AssortmentBox(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StorageUnitType(models.Model):
    name = models.CharField(max_length=255)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    depth = models.IntegerField(null=True)
    label_template = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class StorageUnit(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    assortment_box = models.ForeignKey(AssortmentBox, on_delete=models.CASCADE)
    storage_unit_type = models.ForeignKey(
        StorageUnitType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.assortment_box.name}/{self.number}'


class StorageUnitCompartment(models.Model):
    name = models.CharField(max_length=255, null=True)
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.storage_unit.assortment_box.name}/{self.storage_unit.number}/{self.name}'


class Merchant(models.Model):
    name = models.CharField(max_length=254, null=True)

    def __str__(self):
        return self.name


class ComponentType(models.Model):
    name = models.CharField(max_length=64)


class Component(models.Model):
    storage_unit_compartment = models.ForeignKey(
        StorageUnitCompartment, on_delete=models.CASCADE, null=True, blank=True)
    part_number = models.CharField(max_length=64, primary_key=True)
    resell_price = models.DecimalField(
        null=True, max_digits=20, decimal_places=5)
    usual_order_quantity = models.IntegerField(default=1)
    primary_datasheet = models.CharField(max_length=254, null=True)
    detailed_description = models.CharField(max_length=254, null=True)
    product_description = models.CharField(max_length=254, null=True)
    order_unit_price = models.FloatField(null=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    # type = models.ForeignKey(
    #     ComponentType, on_delete=models.CASCADE)

    def __str__(self):
        return self.part_number

    def update_cache(self):
        raise NotImplementedError()


class SubComponent(models.Model):
    name = models.CharField(max_length=64)


class Category(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)


class DigiKeyComponent(Component):
    cache_expiry = models.DateTimeField(default=timezone.now)

    def update_cache(self):
        pd = digikey.product_details(self.part_number)
        self.primary_datasheet = pd.primary_datasheet
        self.detailed_description = pd.detailed_description
        self.product_description = pd.product_description
        for price in pd.standard_pricing:
            if price.break_quantity >= self.usual_order_quantity:
                self.order_unit_price = price.unit_price
        dt = timezone.now()
        dt = dt + datetime.timedelta(days=10)
        self.cache_expiry = dt


class Inventory(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    count = models.IntegerField()

    def __str__(self):
        return f'{self.component.part_number} ({self.count})'


class Purchase(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=64)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.merchant.name} order number {self.order_number} from {self.timestamp}'


class PurchaseLine(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.purchase.merchant.name} order number {self.purchase.order_number}: {self.component.part_number}'
