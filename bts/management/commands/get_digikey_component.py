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
        for price in part.standard_pricing:
            if price.break_quantity >= usual_order_quantity:
                part.order_unit_price = price.unit_price
                break
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

    def handle(self, *args, **options):
        os.environ["DIGIKEY_CLIENT_ID"] = settings.DIGIKEY_CLIENT_ID
        os.environ["DIGIKEY_CLIENT_SECRET"] = settings.DIGIKEY_CLIENT_SECRET
        os.environ["DIGIKEY_CLIENT_SANDBOX"] = settings.DIGIKEY_CLIENT_SANDBOX
        os.environ["DIGIKEY_STORAGE_PATH"] = settings.DIGIKEY_STORAGE_PATH

        part = self.get_part(options["part_number"], options["usual_order_quantity"])

        ct_path = [part.category.value]
        ct_path.extend(part.family.value.split(" - "))

        ct = self.get_component_type(ct_path)

        c = Component.objects.filter(part_number=options["part_number"])
        if len(c) > 0:
            print(f"Updating component {c[0]}")
            c = c[0]
            c.primary_datasheet = part.primary_datasheet
            c.detailed_description = part.detailed_description
            c.product_description = part.product_description
            c.save()

            sc = c.subcomponent_set.all()[0]
            sc.name = c.product_description
            sc.component_type = ct
            sc.resell_price = self.resell_price(part.order_unit_price)
            sc.order_unit_price = part.order_unit_price
            sc.save()
        else:
            print(f"Creating component {options['part_number']}")
            c = Component.objects.create(
                part_number=options["part_number"],
                merchant=Merchant.objects.get(name="DigiKey"),
                primary_datasheet=part.primary_datasheet,
                detailed_description=part.detailed_description,
                product_description=part.product_description,
            )

            sc = SubComponent.objects.create(
                name=c.product_description,
                component=c,
                component_type=ct,
                resell_price=self.resell_price(part.order_unit_price),
                order_unit_price=part.order_unit_price,
            )
