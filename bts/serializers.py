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

from rest_framework import serializers

from bts.models import *


class LabelTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LabelType
        fields = [
            "id",
            "name",
            "width",
            "height",
            "lines_per_row",
            "rows_per_label",
        ]


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = [
            "id",
            "name",
        ]


class AssortmentBoxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AssortmentBox
        fields = [
            "id",
            "name",
            "location",
            "coordinates",
            "color",
            "layout",
        ]


class StorageUnitTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StorageUnitType
        fields = [
            "id",
            "name",
            "width",
            "height",
            "depth",
            "label_template",
        ]


class StorageUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StorageUnit
        fields = [
            "id",
            "name",
            "number",
            "assortment_box",
            "storage_unit_type",
        ]


class StorageUnitCompartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StorageUnitCompartment
        fields = [
            "id",
            "name",
            "labeltext",
            "storage_unit",
            "z_index",
        ]


class MerchantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Merchant
        fields = [
            "id",
            "name",
            "url",
            "description",
        ]


class ComponentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentType
        fields = [
            "id",
            "name",
            "parent",
        ]


class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component
        fields = [
            "id",
            "part_number",
            "usual_order_quantity",
            "primary_datasheet",
            "detailed_description",
            "product_description",
            "merchant",
            "cache_expiry",
            "notes",
        ]


class SubComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubComponent
        fields = [
            "id",
            "name",
            "resell_price",
            "storage_unit_compartments",
            "component",
            "order_unit_price",
            "component_type",
        ]


class InventorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            "id",
            "sub_component",
            "storage_unit_compartment",
            "timestamp",
            "count",
            "exact_match",
        ]


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            "id",
            "merchant",
            "order_number",
            "timestamp",
        ]


class PurchaseLineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PurchaseLine
        fields = [
            "id",
            "component",
            "quantity",
            "unit_price",
            "purchase",
        ]
