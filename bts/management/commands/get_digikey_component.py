from django.core.management.base import BaseCommand
from bts.models import *
import os
import digikey
from digikey.v3.productinformation import KeywordSearchRequest
import logging

from django.conf import settings


class Command(BaseCommand):
    def get_part(self, part_number, usual_order_quantity):
        part = digikey.product_details(part_number)
        prices = {i.break_quantity: i.unit_price for i in part.standard_pricing}
        for break_quantity in sorted(prices.keys()):
            price_quantity = break_quantity
            if break_quantity >= usual_order_quantity:
                break
        part.order_unit_price = prices[price_quantity]
        return part

    def resell_price(self, order_unit_price) -> float:
        return round(order_unit_price + 0.005, 2)

    def add_arguments(self, parser) -> None:
        parser.add_argument("part_number", type=str)
        parser.add_argument("usual_order_quantity", type=int)

    def get_component_type(self, ct_path) -> ComponentType:
        component_types = ComponentType.objects.filter(name=ct_path[-1])
        if len(component_types) > 0:
            return component_types[0]

        if len(ct_path) > 1:
            parent = self.get_component_type(ct_path[:-1])
        else:
            parent = None
        print(f"Creating component type: {ct_path[-1]} with parent {parent}")
        return ComponentType.objects.create(name=ct_path[-1], parent=parent)

    def create_or_update_component(self, part_number, usual_order_quantity) -> Component:
        part = self.get_part(part_number, usual_order_quantity)
        c = Component.objects.filter(part_number=part_number, merchant__name="DigiKey")
        if len(c) == 0:
            ct_path = [part.category.value]
            ct_path.extend(part.family.value.split(" - "))

            ct = self.get_component_type(ct_path)

            component = Component.objects.create(
                part_number=part_number,
                merchant=Merchant.objects.get(name="DigiKey"),
                primary_datasheet=part.primary_datasheet,
                detailed_description=part.detailed_description,
                product_description=part.product_description,
                usual_order_quantity=usual_order_quantity,
            )
            print(f"Created component {component}")
        elif len(c) > 1:
            raise Exception(f"Multiple components with part number {part_number}")
        else:
            component = c[0]
            component.primary_datasheet = part.primary_datasheet
            component.detailed_description = part.detailed_description
            component.product_description = part.product_description
            component.usual_order_quantity = usual_order_quantity
            component.save()
            print(f"Updated component {component}")

        return component

    def create_or_update_subcomponent(self, component, part_number, usual_order_quantity):
        part = self.get_part(part_number, usual_order_quantity)
        sc = SubComponent.objects.filter(component=component)

        if len(sc) == 0:
            # SubComponent needs to be created
            ct_path = [part.category.value]
            ct_path.extend(part.family.value.split(" - "))

            ct = self.get_component_type(ct_path)

            sc = SubComponent.objects.create(
                name=component.product_description,
                component=component,
                component_type=ct,
                resell_price=self.resell_price(part.order_unit_price),
                order_unit_price=part.order_unit_price,
            )
            print(f"Created subcomponent {sc}")

    def handle(self, *args, **options):
        os.environ["DIGIKEY_CLIENT_ID"] = settings.DIGIKEY_CLIENT_ID
        os.environ["DIGIKEY_CLIENT_SECRET"] = settings.DIGIKEY_CLIENT_SECRET
        os.environ["DIGIKEY_CLIENT_SANDBOX"] = settings.DIGIKEY_CLIENT_SANDBOX
        os.environ["DIGIKEY_STORAGE_PATH"] = settings.DIGIKEY_STORAGE_PATH

        component = self.create_or_update_component(
            options["part_number"], options["usual_order_quantity"]
        )
        sub_component = self.create_or_update_subcomponent(
            component, options["part_number"], options["usual_order_quantity"]
        )
