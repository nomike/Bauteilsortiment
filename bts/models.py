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

from django.db import models
from django.utils import timezone

# Create your models here.


class LabelType(models.Model):
    """
    A label type is a type of label that can be printed for an assortment box.
    """

    name = models.CharField(max_length=255, unique=True)
    width = models.IntegerField()
    height = models.IntegerField()
    lines_per_row = models.IntegerField()
    rows_per_label = models.IntegerField()

    def __str__(self):
        return f"/* {self.name} */--label-height: {self.height}mm; --label-width: {self.width}mm; --label-lines-per-row: {self.lines_per_row}; --label-rows-per-label: {self.rows_per_label};"

    class Meta:
        ordering = ["name"]


class Location(models.Model):
    """
    A location is a place (i.e. a room) where AssortmentBoxes are placed.
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class AssortmentBox(models.Model):
    """
    A box cotaining components. Assortment boxes are divided into storage units which are divided into compartments.
    """

    name = models.CharField(max_length=255, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    coordinates = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Spreadsheet style coordinates (e.g. A1, B5, ...)",
    )
    color = models.CharField(max_length=255, null=True, blank=True)
    layout = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Layout of the storage units in the assortment box in columns and rows (e.g. 5x12, 5x12+2x3+1, ...)",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "assortment boxes"
        ordering = ["name"]


class StorageUnitType(models.Model):
    """
    A type of storage unit.
    """

    name = models.CharField(max_length=255, unique=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    depth = models.IntegerField(null=True)
    label_type = models.ForeignKey(LabelType, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class StorageUnit(models.Model):
    """
    A storage unit is a box containing compartments. In most cases these are transparent plastic drawers.
    """

    name = models.CharField(max_length=255)
    number = models.IntegerField()
    assortment_box = models.ForeignKey(AssortmentBox, on_delete=models.CASCADE)
    storage_unit_type = models.ForeignKey(StorageUnitType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.assortment_box.name}/{self.number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["number", "assortment_box"],
                name="UQ_StorageUnit_number_assortment_box",
            )
        ]
        ordering = ["assortment_box", "number"]


class StorageUnitCompartment(models.Model):
    """
    Storage units could be subdivided into compartments.
    """

    name = models.CharField(max_length=255, null=True)
    labeltext = models.CharField(max_length=255, null=True, blank=True)
    storage_unit = models.ForeignKey(
        StorageUnit, related_name="storage_unit_compartments", on_delete=models.CASCADE
    )
    z_index = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.storage_unit.assortment_box.name}/{self.storage_unit.number}/{self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "storage_unit"],
                name="UQ_StorageUnitCompartment_name_storage_unit",
            ),
            models.UniqueConstraint(
                fields=["z_index", "storage_unit"],
                name="UQ_StorageUnitCompartment_z_index_storage_unit",
            ),
        ]
        ordering = ["storage_unit", "z_index"]


class Merchant(models.Model):
    """
    A merchant is a company that sells electronic components.
    """

    name = models.CharField(max_length=255, null=True, unique=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ComponentType(models.Model):
    """
    A component type is a category of components. They can have parents and thus form a tree. Usually components are located at the leafs of the tree.
    """

    name = models.CharField(max_length=64, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Component(models.Model):
    """
    A component is a single orderable item. It can sonsist of multiple subcomponents. E.g. a resistor-kit would be a component, the individual resistors would be subcomponents.
    """

    part_number = models.CharField(max_length=64, verbose_name="Part number")
    usual_order_quantity = models.IntegerField(default=1)
    primary_datasheet = models.URLField(max_length=254, null=True, blank=True)
    detailed_description = models.CharField(max_length=254, null=True, blank=True)
    product_description = models.CharField(max_length=254, null=True, blank=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    cache_expiry = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.part_number} - {self.product_description}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["part_number", "merchant"],
                name="UQ_Component_part_number_merchant",
            )
        ]
        ordering = ["product_description", "merchant"]


class SubComponent(models.Model):
    """
    A subcomponent is a component that is part of another component. E.g. a resistor is a subcomponent of a resistor-kit.
    """

    name = models.CharField(max_length=64)
    resell_price = models.DecimalField(null=True, max_digits=20, decimal_places=5)
    storage_unit_compartments = models.ManyToManyField(
        StorageUnitCompartment, through="Inventory", blank=True
    )

    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    order_unit_price = models.FloatField(null=True, blank=True)
    component_type = models.ForeignKey(
        ComponentType, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.component.__str__()}/{self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "component"], name="UQ_SubComponent_name_component"
            )
        ]
        ordering = ["component", "name"]


class Inventory(models.Model):
    """
    An inventory is a single type of subcomponents in a single storage unit compartment.
    """

    sub_component = models.ForeignKey(SubComponent, on_delete=models.CASCADE)
    storage_unit_compartment = models.ForeignKey(
        StorageUnitCompartment, related_name="inventories", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(default=timezone.now)
    count = models.IntegerField()
    exact_match = models.BooleanField(
        default=True,
        help_text="Is this the actual SubComponent, or is it just one with similar enough specs?",
    )

    def __str__(self):
        return f"{self.sub_component.component.product_description}/{self.sub_component.name} ({self.count})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sub_component", "storage_unit_compartment"],
                name="UQ_Inventory_sub_component_storage_unit_compartment",
            )
        ]
        ordering = ["storage_unit_compartment", "sub_component"]
        verbose_name_plural = "invetories"


class Purchase(models.Model):
    """
    A purchase is a single order from a merchant.
    """

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=64)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.merchant.name} order number {self.order_number} from {self.timestamp}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merchant", "order_number"],
                name="UQ_Purchase_merchant_oder_number",
            )
        ]
        ordering = ["merchant", "timestamp"]


class PurchaseLine(models.Model):
    """
    A purchase line is a single line in a purchase.
    """

    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.purchase.merchant.name} order number {self.purchase.order_number}: {self.component.part_number}"

    class Meta:
        ordering = ["purchase", "component"]
