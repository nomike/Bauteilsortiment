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

# import digikey
# from digikey.v3.productinformation import KeywordSearchRequest
from django.db import models
from django.utils import timezone

# Create your models here.

# os.environ['DIGIKEY_CLIENT_ID'] = 'i1DbG9gggftX71MLTUngzAayWRMUzMGO'
# os.environ['DIGIKEY_CLIENT_SECRET'] = 'piWwjB6V8TYsxlLg'
# os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
# os.environ['DIGIKEY_STORAGE_PATH'] = './cache'


class AssortmentBox(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "assortment boxes"

    def __str__(self):
        return self.name


class StorageUnitType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    depth = models.IntegerField(null=True)
    label_template = models.CharField(max_length=255, null=True, blank=True)

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["number", "assortment_box"], name="UQ_StorageUnit_number_assortment_box")
        ]


class StorageUnitCompartment(models.Model):
    name = models.CharField(max_length=255, null=True)
    storage_unit = models.ForeignKey(
        StorageUnit, related_name="storage_unit_compartments", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.storage_unit.assortment_box.name}/{self.storage_unit.number}/{self.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "storage_unit"], name="UQ_StorageUnitCompartment_name_storage_unit")
        ]


class Merchant(models.Model):
    name = models.CharField(max_length=255, null=True, unique=True)
    url = models.URLField(max_length=255, null=True)

    def __str__(self):
        return self.name


class ComponentType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Component(models.Model):
    part_number = models.CharField(
        max_length=64, verbose_name="Part number")
    usual_order_quantity = models.IntegerField(default=1)
    primary_datasheet = models.URLField(max_length=254, null=True, blank=True)
    detailed_description = models.CharField(
        max_length=254, null=True, blank=True)
    product_description = models.CharField(
        max_length=254, null=True, blank=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    cache_expiry = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.part_number} - {self.product_description}'

    class Meta:
        unique_together = ("part_number", "merchant")

    # def update_cache(self, force: bool = False):
    #     if force or self.cache_expiry < timezone.now():
    #         if self.merchant == Merchant.objects.get(name="DigiKey"):
    #             pd = digikey.product_details(self.part_number)
    #             self.primary_datasheet = pd.primary_datasheet
    #             self.detailed_description = pd.detailed_description
    #             self.product_description = pd.product_description
    #             for price in pd.standard_pricing:
    #                 if price.break_quantity >= self.usual_order_quantity:
    #                     self.order_unit_price = price.unit_price
    #             dt = timezone.now()
    #             dt = dt + datetime.timedelta(days=10)
    #             self.cache_expiry = dt
    #         else:
    #             pass


class SubComponent(models.Model):
    name = models.CharField(max_length=64)
    resell_price = models.DecimalField(
        null=True, max_digits=20, decimal_places=5)
    storage_unit_compartments = models.ManyToManyField(
        StorageUnitCompartment, through='Inventory', blank=True)

    component = models.ForeignKey(
        Component, on_delete=models.CASCADE)
    order_unit_price = models.FloatField(null=True, blank=True)
    component_type = models.ForeignKey(
        ComponentType, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.component.product_description}/{self.name}'

    class Meta:
        unique_together = ("name", "component")


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Inventory(models.Model):
    sub_component = models.ForeignKey(SubComponent, on_delete=models.CASCADE)
    storage_unit_compartment = models.ForeignKey(
        StorageUnitCompartment, related_name="inventories", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    count = models.IntegerField()

    def __str__(self):
        return f'{self.sub_component.component.product_description}/{self.sub_component.name} ({self.count})'

    class Meta:
        unique_together = ("sub_component", "storage_unit_compartment")
        verbose_name_plural = "invetories"


class Purchase(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=64)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.merchant.name} order number {self.order_number} from {self.timestamp}'

    class Meta:
        unique_together = ("merchant", "order_number")


class PurchaseLine(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.purchase.merchant.name} order number {self.purchase.order_number}: {self.component.part_number}'
