from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.contrib import admin
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
        self.label_type = LabelType.objects.create(name="Test Label Type", width=10, height=10, lines_per_row=1, rows_per_label=1)

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
