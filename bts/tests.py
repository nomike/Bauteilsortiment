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


import json

from django.contrib import admin
from django.contrib.auth.models import Permission, User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from bts.models import *


class MerchantTestCase(TestCase):
    def setUp(self):
        Merchant.objects.create(name="Test Merchant")

    def test_merchant_name(self):
        merchant = Merchant.objects.get(name="Test Merchant")
        self.assertEqual(merchant.name, "Test Merchant")


class AssortmentBoxTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Test Location")
        AssortmentBox.objects.create(
            name="Test Assortment Box",
            location=self.location,
            coordinates="A5",
            color="Red",
            layout="1x1",
        )

    def test_assortment_box_name(self):
        assortment_box = AssortmentBox.objects.get(name="Test Assortment Box")
        self.assertEqual(assortment_box.name, "Test Assortment Box")

    def test_assortment_box_location(self):
        assortment_box = AssortmentBox.objects.get(name="Test Assortment Box")
        self.assertEqual(assortment_box.location, self.location)

    def test_assortment_box_coordinates(self):
        assortment_box = AssortmentBox.objects.get(name="Test Assortment Box")
        self.assertEqual(assortment_box.coordinates, "A5")

    def test_assortment_box_color(self):
        assortment_box = AssortmentBox.objects.get(name="Test Assortment Box")
        self.assertEqual(assortment_box.color, "Red")

    def test_assortment_box_layout(self):
        assortment_box = AssortmentBox.objects.get(name="Test Assortment Box")
        self.assertEqual(assortment_box.layout, "1x1")


class StorageUnitTestCase(TestCase):
    def setUp(self):
        self.assortment_box = AssortmentBox.objects.create(name="Test Assortment Box")
        StorageUnit.objects.create(number=1, assortment_box=self.assortment_box)

    def test_storage_unit_number(self):
        storage_unit = StorageUnit.objects.get(assortment_box=self.assortment_box, number=1)
        self.assertEqual(storage_unit.number, 1)

    def test_storage_unit_assortment_box(self):
        storage_unit = StorageUnit.objects.get(assortment_box=self.assortment_box, number=1)
        self.assertEqual(storage_unit.assortment_box, self.assortment_box)


class StorageUnitCompartmentTestCase(TestCase):
    def setUp(self):
        self.assortment_box = AssortmentBox.objects.create(name="Test Assortment Box")
        self.storage_unit = StorageUnit.objects.create(assortment_box=self.assortment_box, number=1)
        StorageUnitCompartment.objects.create(
            storage_unit=self.storage_unit, name="Test Storage Unit Compartment"
        )

    def test_storage_unit_compartment_name(self):
        storage_unit_compartment = StorageUnitCompartment.objects.get(
            storage_unit=self.storage_unit, name="Test Storage Unit Compartment"
        )
        self.assertEqual(storage_unit_compartment.name, "Test Storage Unit Compartment")

    def test_storage_unit_compartment_storage_unit(self):
        storage_unit_compartment = StorageUnitCompartment.objects.get(
            storage_unit=self.storage_unit, name="Test Storage Unit Compartment"
        )
        self.assertEqual(storage_unit_compartment.storage_unit, self.storage_unit)

    def test_storage_unit_compartment_assortment_box(self):
        storage_unit_compartment = StorageUnitCompartment.objects.get(
            storage_unit=self.storage_unit, name="Test Storage Unit Compartment"
        )
        self.assertEqual(storage_unit_compartment.storage_unit.assortment_box, self.assortment_box)

    def test_storage_unit_compartment_assortment_box_name(self):
        storage_unit_compartment = StorageUnitCompartment.objects.get(
            storage_unit=self.storage_unit, name="Test Storage Unit Compartment"
        )
        self.assertEqual(
            storage_unit_compartment.storage_unit.assortment_box.name, self.assortment_box.name
        )


class ComponentTypeTestCase(TestCase):
    def setUp(self):
        ComponentType.objects.create(name="Test Component Type")

    def test_component_type_name(self):
        component_type = ComponentType.objects.get(name="Test Component Type")
        self.assertEqual(component_type.name, "Test Component Type")


class ComponentTestCase(TestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create(name="Test Merchant")
        Component.objects.create(
            part_number="Test Part Number",
            product_description="Test Product Description",
            merchant=self.merchant,
        )

    def test_component_part_number(self):
        component = Component.objects.get(part_number="Test Part Number")
        self.assertEqual(component.part_number, "Test Part Number")

    def test_component_product_description(self):
        component = Component.objects.get(part_number="Test Part Number")
        self.assertEqual(component.product_description, "Test Product Description")

    def test_component_merchant(self):
        component = Component.objects.get(part_number="Test Part Number")
        self.assertEqual(component.merchant, self.merchant)


class SubComponentTestCase(TestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create(name="Test Merchant")
        self.component_type = ComponentType.objects.create(name="Test Component Type")
        self.component = Component.objects.create(
            part_number="Test Part Number",
            product_description="Test Product Description",
            merchant=self.merchant,
        )
        self.sub_component = SubComponent.objects.create(
            component=self.component,
            component_type=self.component_type,
            name="Test SubComponent",
        )
        self.model_admin = admin.site._registry[SubComponent]

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_sub_component_name(self):
        sub_component = SubComponent.objects.get(name="Test SubComponent")
        self.assertEqual(sub_component.name, "Test SubComponent")

    def test_sub_component_component(self):
        sub_component = SubComponent.objects.get(name="Test SubComponent")
        self.assertEqual(sub_component.component, self.component)

    def test_sub_component_component_type(self):
        sub_component = SubComponent.objects.get(name="Test SubComponent")
        self.assertEqual(sub_component.component_type, self.component_type)

    def test_sub_component_component_merchant(self):
        sub_component = SubComponent.objects.get(name="Test SubComponent")
        self.assertEqual(sub_component.component.merchant, self.merchant)

    def test_sub_component_admin_search_field(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("admin:bts_subcomponent_changelist"), {"q": "Test Part Number"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.sub_component.name)


class InventoryTestCase(TestCase):
    def setUp(self):
        self.now = timezone.now()
        self.merchant = Merchant.objects.create(name="Test Merchant")
        self.component_type = ComponentType.objects.create(name="Test Component Type")
        self.component = Component.objects.create(
            part_number="Test Part Number",
            product_description="Test Product Description",
            merchant=self.merchant,
        )
        self.sub_component = SubComponent.objects.create(
            component=self.component,
            component_type=self.component_type,
            name="Test SubComponent",
        )
        self.assortment_box = AssortmentBox.objects.create(name="Test Assortment Box")
        self.storage_unit = StorageUnit.objects.create(assortment_box=self.assortment_box, number=1)
        self.storage_unit_compartment = StorageUnitCompartment.objects.create(
            storage_unit=self.storage_unit, name="Test Storage Unit Compartment"
        )
        Inventory.objects.create(
            sub_component=self.sub_component,
            storage_unit_compartment=self.storage_unit_compartment,
            timestamp=self.now,
            count=1,
        )

    def test_inventory_count(self):
        inventory = Inventory.objects.get(sub_component=self.sub_component)
        self.assertEqual(inventory.count, 1)

    def test_inventory_timestamp(self):
        inventory = Inventory.objects.get(sub_component=self.sub_component)
        self.assertEqual(inventory.timestamp, self.now)

    def test_inventory_storage_unit_compartment(self):
        inventory = Inventory.objects.get(sub_component=self.sub_component)
        self.assertEqual(inventory.storage_unit_compartment, self.storage_unit_compartment)

    def test_inventory_sub_component(self):
        inventory = Inventory.objects.get(sub_component=self.sub_component)
        self.assertEqual(inventory.sub_component, self.sub_component)

    def test_inventory_storage_unit(self):
        inventory = Inventory.objects.get(sub_component=self.sub_component)
        self.assertEqual(inventory.storage_unit_compartment.storage_unit, self.storage_unit)

    def test_inventory_assortment_box(self):
        inventory = Inventory.objects.get(sub_component=self.sub_component)
        self.assertEqual(
            inventory.storage_unit_compartment.storage_unit.assortment_box, self.assortment_box
        )


class StorageUnitTypeTestCase(TestCase):
    def setUp(self):
        StorageUnitType.objects.create(name="Test Storage Unit Type")

    def test_storage_unit_type_name(self):
        storage_unit_type = StorageUnitType.objects.get(name="Test Storage Unit Type")
        self.assertEqual(storage_unit_type.name, "Test Storage Unit Type")


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.now = timezone.now()
        self.merchant = Merchant.objects.create(name="Test Merchant")
        self.component_type = ComponentType.objects.create(name="Test Component Type")
        self.component = Component.objects.create(
            part_number="Test Part Number",
            product_description="Test Product Description",
            merchant=self.merchant,
        )
        self.sub_component = SubComponent.objects.create(
            component=self.component,
            component_type=self.component_type,
            name="Test SubComponent",
        )
        self.assortment_box = AssortmentBox.objects.create(name="Test Assortment Box")
        self.storage_unit = StorageUnit.objects.create(assortment_box=self.assortment_box, number=1)
        self.storage_unit_compartment = StorageUnitCompartment.objects.create(
            storage_unit=self.storage_unit, name="Test Storage Unit Compartment"
        )
        self.purchase = Purchase.objects.create(
            merchant=self.merchant, order_number="Test Order Number", timestamp=self.now
        )


class PurchaseLineTestCase(TestCase):
    def setUp(self):
        self.now = timezone.now()
        self.merchant = Merchant.objects.create(name="Test Merchant")
        self.component_type = ComponentType.objects.create(name="Test Component Type")
        self.component = Component.objects.create(
            part_number="Test Part Number",
            product_description="Test Product Description",
            merchant=self.merchant,
        )
        self.sub_component = SubComponent.objects.create(
            component=self.component,
            component_type=self.component_type,
            name="Test SubComponent",
        )
        self.assortment_box = AssortmentBox.objects.create(name="Test Assortment Box")
        self.storage_unit = StorageUnit.objects.create(assortment_box=self.assortment_box, number=1)
        self.storage_unit_compartment = StorageUnitCompartment.objects.create(
            storage_unit=self.storage_unit, name="Test Storage Unit Compartment"
        )
        self.purchase = Purchase.objects.create(
            merchant=self.merchant, order_number="Test Order Number", timestamp=self.now
        )
        PurchaseLine.objects.create(
            purchase=self.purchase,
            component=self.component,
            quantity=1,
            unit_price=1,
        )

    def test_purchase_line_quantity(self):
        purchase_line = PurchaseLine.objects.get(component=self.component)
        self.assertEqual(purchase_line.quantity, 1)

    def test_purchase_line_purchase(self):
        purchase_line = PurchaseLine.objects.get(component=self.component)
        self.assertEqual(purchase_line.purchase, self.purchase)


class LocationTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Test Location")

    def test_location_name(self):
        location = Location.objects.get(name="Test Location")
        self.assertEqual(location.name, "Test Location")


class LabelTypeTestCase(TestCase):
    def setUp(self):
        self.label_type = LabelType.objects.create(
            name="Test Label Type", width=10, height=10, lines_per_row=1, rows_per_label=1
        )

    def test_label_type_name(self):
        label_type = LabelType.objects.get(name="Test Label Type")
        self.assertEqual(label_type.name, "Test Label Type")

    def test_label_type_width(self):
        label_type = LabelType.objects.get(name="Test Label Type")
        self.assertEqual(label_type.width, 10)

    def test_label_type_height(self):
        label_type = LabelType.objects.get(name="Test Label Type")
        self.assertEqual(label_type.height, 10)

    def test_label_type_lines_per_row(self):
        label_type = LabelType.objects.get(name="Test Label Type")
        self.assertEqual(label_type.lines_per_row, 1)

    def test_label_type_rows_per_label(self):
        label_type = LabelType.objects.get(name="Test Label Type")
        self.assertEqual(label_type.rows_per_label, 1)


class LabelTypeAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("labeltype-list")
        self.data = {
            "name": "Test Label Type",
            "width": 10,
            "height": 10,
            "lines_per_row": 1,
            "rows_per_label": 1,
        }
        self.invalid_data = {
            "name": "",
            "width": 10,
            "height": 10,
            "lines_per_row": 1,
            "rows_per_label": 1,
        }

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_label_type(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_label_type(self):
        response = self.client.post(
            self.url, json.dumps(self.invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_label_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LocationAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("location-list")
        self.data = {"name": "Test Location"}
        self.invalid_data = {"name": ""}

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_location(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_location(self):
        response = self.client.post(
            self.url, json.dumps(self.invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AssortmentBoxAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("assortmentbox-list")
        self.data = {"name": "Test Assortment Box"}
        self.invalid_data = {"name": ""}

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_component_type(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_component_type(self):
        response = self.client.post(
            self.url, json.dumps(self.invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_component_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StorageUnitTypeAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("storageunittype-list")
        self.data = {"name": "Test Storage Unit Type"}
        self.invalid_data = {"name": ""}

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_storage_unit_type(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_storage_unit_type(self):
        response = self.client.post(
            self.url, json.dumps(self.invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_storage_unit_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StorageUnitAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("storageunit-list")
        self.location = Location.objects.create(name="Test Location")
        self.assortment_box = AssortmentBox.objects.create(name="Test Assortment Box")
        self.data = {
            "name": "Test Storage Unit",
            "number": 1,
            "assortment_box": reverse(
                "assortmentbox-detail", kwargs={"pk": self.assortment_box.pk}
            ),
        }
        self.invalid_data = {"name": ""}

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_storage_unit(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_storage_unit(self):
        response = self.client.post(
            self.url, json.dumps(self.invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_storage_unit(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StorageUnitCompartmentAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("storageunitcompartment-list")
        self.location = Location.objects.create(name="Test Location")
        self.assortment_box = AssortmentBox.objects.create(name="Test Assortment Box")

        self.storage_unit = StorageUnit.objects.create(
            name="Test Storage Unit", number=1, assortment_box=self.assortment_box
        )
        self.data = {
            "name": "Test Storage Unit Compartment",
            "number": 1,
            "storage_unit": reverse("storageunit-detail", kwargs={"pk": self.storage_unit.pk}),
        }
        self.invalid_data = {"name": ""}

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_storage_unit_compartment(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_storage_unit_compartment(self):
        response = self.client.post(
            self.url, json.dumps(self.invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_storage_unit_compartment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MerchantAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("merchant-list")
        self.data = {"name": "Test Merchant"}
        self.invalid_data = {"name": ""}

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_merchant(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Merchant.objects.count(), 1)
        self.assertEqual(Merchant.objects.get().name, "Test Merchant")

    # def test_create_Merchant_with_invalid_data(self):
    #     response = self.client.post(self.url, self.invalid_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(Merchant.objects.count(), 0)

    def test_retrieve_Merchant(self):
        merchant = Merchant.objects.create(name="Test Merchant")
        url = reverse("merchant-detail", args=[merchant.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Merchant")  # type: ignore

    def test_update_Merchant(self):
        merchant = Merchant.objects.create(name="Test Merchant")
        url = reverse("merchant-detail", args=[merchant.pk])
        updated_data = {
            "name": "Updated Merchant",
            "url": merchant.url,
            "description": merchant.description,
        }
        response = self.client.put(url, json.dumps(updated_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Merchant.objects.get(pk=merchant.pk).name, "Updated Merchant")

    def test_delete_Merchant(self):
        merchant = Merchant.objects.create(name="Test Merchant")
        url = reverse("merchant-detail", args=[merchant.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Merchant.objects.count(), 0)


class ComponentTypeAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("componenttype-list")
        self.data = {"name": "Test Component Type"}
        self.invalid_data = {"name": ""}

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_component_type(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_component_type(self):
        response = self.client.post(
            self.url, json.dumps(self.invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_component_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ComponentAPITestCase(APITestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create(name="Test Merchant")
        self.url = reverse("component-list")
        self.data = {
            "name": "Test Component",
            "part_number": "1234567890",
            "usual_order_quantity": 1,
            "merchant": reverse("merchant-detail", args=[self.merchant.id]),  # type: ignore
        }
        self.invalid_data = {"name": ""}

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_component(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_component(self):
        response = self.client.post(
            self.url, json.dumps(self.invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_component(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubComponentAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("subcomponent-list")
        self.merchant = Merchant.objects.create(name="Test Merchant")
        self.component_type = ComponentType.objects.create(name="Test Component Type")
        self.component = Component.objects.create(
            part_number="1234567890",
            usual_order_quantity=1,
            merchant=self.merchant,
        )
        self.data = {
            "name": "Test SubComponent",
            "component": reverse("component-detail", args=[self.component.id]),  # type: ignore
            "component_type": reverse("componenttype-detail", args=[self.component_type.id]),  # type: ignore
        }
        self.invalid_data = {"name": ""}

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_subcomponent(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_subcomponent(self):
        response = self.client.post(
            self.url, json.dumps(self.invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_subcomponent(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InventoryAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("inventory-list")
        self.location = Location.objects.create(name="Test Location")
        self.assortment_box = AssortmentBox.objects.create(
            name="Test Assortment Box", location=self.location
        )
        self.storage_unit = StorageUnit.objects.create(
            name="Test Storage Unit", assortment_box=self.assortment_box, number=1
        )
        self.storage_unit_compartment = StorageUnitCompartment.objects.create(
            storage_unit=self.storage_unit, name="Test Storage Unit Compartment"
        )

        self.merchant = Merchant.objects.create(name="Test Merchant")
        self.component_type = ComponentType.objects.create(name="Test Component Type")
        self.component = Component.objects.create(
            part_number="1234567890",
            usual_order_quantity=1,
            merchant=self.merchant,
        )
        self.subcomponent = SubComponent.objects.create(
            name="Test SubComponent",
            component=self.component,
            component_type=self.component_type,
        )
        self.data = {
            "sub_component": reverse("subcomponent-detail", args=[self.subcomponent.id]),  # type: ignore
            "storage_unit_compartment": reverse(
                "storageunitcompartment-detail", args=[self.storage_unit_compartment.id]  # type: ignore
            ),
            "count": 1,
        }
        self.invalid_data = {"count": ""}

        # Create a user to test admin functionality
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(
            self.username, password=self.password, is_superuser=True
        )
        self.user.is_staff = True
        self.user.save()
        self.permission = Permission.objects.get(codename="view_subcomponent")
        self.user.user_permissions.add(self.permission)

        # Create a client and force login
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_inventory(self):
        response = self.client.post(
            self.url, json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_inventory(self):
        response = self.client.post(
            self.url, json.dumps(self.invalid_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_inventory(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
