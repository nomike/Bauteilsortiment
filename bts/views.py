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

import inspect
import json
from typing import Any, Dict

import drawsvg
import qrcode
import qrcode.image.svg
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

import bts.models
from bts.models import (
    AssortmentBox,
    Category,
    Component,
    ComponentType,
    Inventory,
    Merchant,
    Purchase,
    PurchaseLine,
    StorageUnit,
    StorageUnitCompartment,
    StorageUnitType,
    SubComponent,
)
from bts.templatetags import view_extras

"""Configuration for generic views.

This dictionary allows you to configure views. Keys are the model classes.
Values are dictionaries themselves with the following keys:

# list_fields               A list of fields which will be rendered as columns in list views.
# list_detail_link_fields   Fiels in this list will be rendered as hyperlinks to the listed object.
# list_foreign_link_fields  Fieldnames listed in here will be rendered as links pointing to the foreign object they represent.
# sublists                  A list of model names for which sub-lists will be rendered on detail pages.
"""

view_config = {
    AssortmentBox: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"],
        "sublists": ["StorageUnit"],
    },
    StorageUnitType: {"list_fields": ["name"], "list_detail_link_fields": ["name"]},
    StorageUnit: {
        "list_fields": ["number", "assortment_box"],
        "list_detail_link_fields": ["number"],
        "sublists": ["StorageUnitCompartment"],
    },
    StorageUnitCompartment: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"],
        "sublists": ["Inventory"],
    },
    Merchant: {
        "list_fields": ["name", "url"],
        "list_detail_link_fields": ["name"],
        "sublists": ["Component", "Purchase"],
    },
    ComponentType: {
        "list_fields": ["name", "parent"],
        "list_detail_link_fields": ["name"],
        "sublists": ["SubComponent"],
    },
    Component: {
        "list_fields": ["part_number", "product_description", "merchant"],
        "list_detail_link_fields": ["part_number"],
        "sublists": ["SubComponent", "PurchaseLine"],
    },
    SubComponent: {"list_fields": ["name"], "list_detail_link_fields": ["name"]},
    Category: {"list_fields": ["name"], "list_detail_link_fields": ["name"]},
    Inventory: {
        "list_fields": [
            "id",
            "sub_component",
            "storage_unit_compartment",
            "timestamp",
            "count",
        ],
        "list_detail_link_fields": ["id"],
        "list_foreign_link_fields": ["sub_component"],
    },
    Purchase: {
        "list_fields": ["order_number", "merchant", "timestamp"],
        "list_detail_link_fields": ["order_number"],
        "sublists": ["PurchaseLine"],
    },
    PurchaseLine: {
        "list_fields": ["id", "component", "quantity", "unit_price", "purchase"],
        "list_detail_link_fields": ["id"],
        "list_foreign_link_fields": ["component"],
    },
}


def home_view(request):
    """Home view which lists all model cstegories.

    Args:
        request (HttpRequest): Django Request Object

    Returns:
        HTTPResponse: A HTML rendering of the home view.
    """
    context = {"types": view_config.keys()}
    return render(request, "bts/home.html", context)


# def component_update_cache(request, component_id):
#     component = get_object_or_404(Component, pk=component_id)
#     component.update_cache(force='force' in request.GET)
#     component.save()

#     return HttpResponseRedirect(reverse('component_details', args=(component.id,)))


class ConfiguredListView(ListView):
    """Abstract class for a configurable list view.
    Shows a list of objects for a certain Model.
    """

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Overloads super().get_context_data() to inject the view_config into the
        template's context.

        Returns:
            Dict[str, Any]: The context used in the template.
        """
        context_data = super().get_context_data(**kwargs)
        for key, value in view_config[self.model].items():
            context_data[key] = value
        return context_data


class ConfiguredDetailView(DetailView):
    """Abstract class for a onfigurable detail view.
    Renders a tabular detail page for one object, listing parameters and sub-lists (for foreign objects).
    """

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Overloads super().get_context_data() to inject the view_config into the
        template's context.

        Returns:
            Dict[str, Any]: The context used in the template.
        """
        context_data = super().get_context_data(**kwargs)
        for key, value in view_config[self.model].items():
            context_data[key] = value
        return context_data


def model_json_view(request, model: str):
    """Renders a JSON document with all items of the specified model.

    Args:
        request (HttpRequest): Django Request Object
        model (str): The name of the model you want to represent

    Returns:
        JsonResponse: The JSON document as a JsonResponse HttpResponse object.
    """
    return JsonResponse(list(getattr(bts.models, model).objects.values()), safe=False)


def model_json_filtered_view(request, model: str, filter_model: str, id: int):
    """Renders a JSON document with all items of the specified model filtered by a foreign key.

    Args:
        request (HttpRequest): Django Request Object
        model (str): The name of the model you want to represent
        filter_model (str): The name of the model you want to filter by
        id (int): The id you want to filter by

    Returns:
        JsonResponse: The JSON document as a JsonResponse HttpResponse object.
    """
    data = getattr(bts.models, model).objects.filter(
        **{view_extras.snake_case(filter_model): id}
    )
    return JsonResponse(list(data.values()), safe=False)


def model_json_field_view(request, model: str, id: int, field: str):
    """Renders a JSON document containing a single parameter of an ojbect.

    Args:

        request (HttpRequest): Django Request Object
        model (str): The name of the model you want to represent
        id (int): The object's ID
        field (str): The fiels who's value you want to have

    Returns:
        JsonResponse: The JSON document as a JsonResponse HttpResponse object.
    """
    return JsonResponse(
        getattr(get_object_or_404(getattr(bts.models, model), pk=id), field), safe=False
    )


class ModelListView(ConfiguredListView):
    """A generic list view."""

    model = None
    template_name = "bts/model_list_page.html"


class ModelFilteredListView(ConfiguredListView):
    """A generic filtered list view."""

    model = None
    template_name = "bts/model_list_snippet.html"

    def get_queryset(self) -> QuerySet[Any]:
        self.filter_object = get_object_or_404(
            getattr(bts.models, self.kwargs["model"]), pk=self.kwargs["id"]
        )
        return self.model.objects.filter(
            **{view_extras.snake_case(self.kwargs["model"]): self.filter_object}
        )


class ModelDetailView(ConfiguredDetailView):
    """A generic detail view."""

    model = None
    template_name = "bts/model_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["fields"] = self.model._meta.fields
        return context


def labelpage(request, id):
    """Render a HTML page full of printable lables.
    The lables could be put on the StorageUnits.

    Args:
        request (HttpRequest): Django Request Object
        id (int): The object's ID

    Returns:
        HttpResponse: The rendered label page.
    """
    assortment_box = get_object_or_404(AssortmentBox, pk=id)
    context = {
        "assortment_box": assortment_box,
        "storage_units": StorageUnit.objects.filter(assortment_box=assortment_box),
    }
    return render(request, "bts/labelpage.html", context)


def qr_code_svg(request, model, id):
    """Renders a SVG image containing a qr code with a link to a specific object.

    Args:
        request (HttpRequest): Django Request Object
        model (str): The name of the model you want to represent
        id (int): The object's ID

    Request arguments:
        GET.box_size (int): Specify the size of one box of the QR code in pixels.

    Returns:
        HttpResponse: A response object containing the SVG image.
    """
    box_size = request.GET.get("box_size")

    img = qrcode.make(
        request.build_absolute_uri(reverse(f"{model}_detail", args=[id])),
        image_factory=qrcode.image.svg.SvgImage,
        box_size=box_size or 4,
        border=1,
    )

    return HttpResponse(img.to_string(encoding="unicode"), content_type="image/svg+xml")


""" Loop through all model types and create generic list and detail views for them.
"""
for name in [
    obj.__name__
    for name, obj in bts.models.__dict__.items()
    if inspect.isclass(obj) and issubclass(obj, models.Model)
]:
    generated_class = type(
        name + "DetailView", (ModelDetailView,), {"model": getattr(bts.models, name)}
    )
    globals()[generated_class.__name__] = generated_class
    generated_class = type(
        name + "ListView", (ModelListView,), {"model": getattr(bts.models, name)}
    )
    globals()[generated_class.__name__] = generated_class
    generated_class = type(
        name + "FilteredListView",
        (ModelFilteredListView,),
        {"model": getattr(bts.models, name)},
    )
    globals()[generated_class.__name__] = generated_class
