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
from typing import Any, Dict

import qrcode
import qrcode.image.svg
import django_filters

from django.db import models
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, ListView
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

import bts.models
from bts.models import (
    AssortmentBox,
    Component,
    ComponentType,
    Inventory,
    LabelType,
    Merchant,
    Purchase,
    PurchaseLine,
    StorageUnit,
    StorageUnitCompartment,
    StorageUnitType,
    SubComponent,
)
from bts.serializers import *

"""
Configuration for generic views.

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
        "sublists": ["storageunit_set"],
    },
    StorageUnitType: {"list_fields": ["name"], "list_detail_link_fields": ["name"]},
    StorageUnit: {
        "list_fields": ["number", "assortment_box"],
        "list_detail_link_fields": ["number"],
        "sublists": ["storage_unit_compartments"],
    },
    StorageUnitCompartment: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"],
        "sublists": ["inventories"],
    },
    Merchant: {
        "list_fields": ["name", "url"],
        "list_detail_link_fields": ["name"],
        "sublists": ["component_set", "purchase_set"],
    },
    ComponentType: {
        "list_fields": ["name", "parent"],
        "list_detail_link_fields": ["name"],
        "sublists": ["componenttype_set", "subcomponent_set"],
        # "sublists": ["componenttype_set"],
    },
    Component: {
        "list_fields": ["part_number", "product_description", "merchant"],
        "list_detail_link_fields": ["part_number"],
        "sublists": ["subcomponent_set", "purchaseline_set"],
    },
    SubComponent: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"],
        "sublists": ["inventory_set"],
    },
    Inventory: {
        "list_fields": ["id", "sub_component", "storage_unit_compartment", "timestamp", "count"],
        "list_detail_link_fields": ["id"],
        "list_foreign_link_fields": ["sub_component"],
    },
    Purchase: {
        "list_fields": ["order_number", "merchant", "timestamp"],
        "list_detail_link_fields": ["order_number"],
        "sublists": ["purchaseline_set"],
    },
    PurchaseLine: {
        "list_fields": ["id", "component", "quantity", "unit_price", "purchase"],
        "list_detail_link_fields": ["id"],
        "list_foreign_link_fields": ["component"],
    },
    LabelType: {
        "list_fields": ["name", "width", "height", "rows_per_label", "lines_per_row"],
        "list_detail_link_fields": ["name"],
    },
}


class PageNumberPaginationLarge(PageNumberPagination):
    page_size = 100
    max_page_size = 10000
    page_size_query_param = "_page_size"
    page_query_param = "_page"

def home_view(request):
    """
    Home view which lists all model categories.

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
    """
    Abstract class for a configurable list view.
    Shows a list of objects for a certain Model.
    """

    def get_queryset(self) -> QuerySet[Any]:
        """
        Overloads super().get_queryset() to use django_filter to filter the queryset.

        Returns:
            QuerySet[Any]: The queryset used to render the list.
        """
        queryset = super().get_queryset()
        self.filter = ComponentFilter(self.request.GET, queryset=queryset)
        return self.filter.qs
        # return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Overloads super().get_context_data() to inject the view_config into the
        template's context.

        Returns:
            Dict[str, Any]: The context used in the template.
        """
        context_data = super().get_context_data(**kwargs)
        for key, value in view_config[self.model].items():
            context_data[key] = value
        context_data["app_label"] = self.model._meta.app_label
        context_data["model_name"] = self.model._meta.model_name
        return context_data


class ConfiguredDetailView(DetailView):
    """
    Abstract class for a configurable detail view.
    Renders a tabular detail page for one object, listing parameters and sub-lists (for foreign objects).
    """

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Overloads super().get_context_data() to inject the view_config into the
        template's context.

        Returns:
            Dict[str, Any]: The context used in the template.
        """
        context_data = super().get_context_data(**kwargs)
        for key, value in view_config[self.model].items():
            context_data[key] = value
        context_data["app_label"] = self.model._meta.app_label
        context_data["model_name"] = self.model._meta.model_name
        return context_data


class GenericViewSet(viewsets.ModelViewSet):
    """
    A generic viewset for a model.
    """

    queryset = None
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Any]:
        queryset = self.model.objects.all()
        # Filter by all query parameters
        for key, value in [i for i in self.request.query_params.items() if i[0][0] != '_']:
            queryset = queryset.filter(**{key: value})
        return queryset


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class ModelListView(ConfiguredListView):
    """
    A generic list view.
    """

    paginate_by = 10
    model = None
    template_name = "bts/model_list_page.html"


class ModelFilteredListView(ConfiguredListView):
    """
    A generic filtered list view.
    """

    model = None
    template_name = "bts/model_list_snippet.html"

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(**{self.kwargs["field"]: self.kwargs["value"]})


class ModelDetailView(ConfiguredDetailView):
    """
    A generic detail view.
    """

    model = None
    template_name = "bts/model_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["fields"] = self.model._meta.fields
        return context


def labelpage(request, id):
    """
    Render a HTML page full of printable lables.
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
        "label_width": request.GET.get("label_width"),
        "label_height": request.GET.get("label_height"),
        "lines_per_row": request.GET.get("lines_per_row"),
    }
    return render(request, "bts/labels/generic/labelpage.html", context)


def qr_redirect(request, id):
    """
    Generates a QR code which redirects to the detail page of the object with the given id.
    Used to make the URL as short as possible, in order to make the qrcodes less dense and thus more readable.
    This sacrifices support for multiple models though and thus makes the qrcodes less flexible.

    For a more generic version see qr_code_svg.

    Args:
        request (HttpRequest): Django Request Object
        id (int): The object's ID

    Returns:
        HttpResponse: A response object containing the SVG image.
    """
    box_size = request.GET.get("box_size")

    img = qrcode.make(
        f"http://b.nomi.ke/bts/qrr/{id}",
        image_factory=qrcode.image.svg.SvgImage,
        box_size=box_size or 4,
        border=1,
    )

    return HttpResponse(img.to_string(encoding="unicode"), content_type="image/svg+xml")


def qr_code_svg(request, model, id):
    """
    Renders a SVG image containing a qr code with a link to a specific object.
    For a more specialized version wich produces less dense qrcodes see qr_redirect.

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
        f'http://b.nomi.ke{reverse(f"{model}_detail", args=[id])}',
        image_factory=qrcode.image.svg.SvgImage,
        box_size=box_size or 4,
        border=1,
    )

    return HttpResponse(img.to_string(encoding="unicode"), content_type="image/svg+xml")


class ComponentFilter(django_filters.FilterSet):
    class Meta:
        model = Component
        fields = {
            "part_number": ["exact", "icontains"],
            "product_description": ["exact", "icontains"],
            "merchant": ["exact"],
        }


# Generate generic views for all the models
for name in [
    obj.__name__
    for name, obj in bts.models.__dict__.items()
    if inspect.isclass(obj) and issubclass(obj, models.Model)
]:
    # generate detail view class
    generated_class = type(
        f"{name}DetailView",
        (ModelDetailView,),
        {"model": getattr(bts.models, name)},
    )
    globals()[generated_class.__name__] = generated_class

    # generate list view class
    generated_class = type(
        f"{name}ListView",
        (ModelListView,),
        {"model": getattr(bts.models, name)},
    )
    globals()[generated_class.__name__] = generated_class

    # generate filtered list view class
    generated_class = type(
        f"{name}FilteredListView",
        (ModelFilteredListView,),
        {"model": getattr(bts.models, name)},
    )
    globals()[generated_class.__name__] = generated_class

    # generate API viewset class
    generated_class = type(
        f"{name}ViewSet",
        (GenericViewSet,),
        {   
            "model": getattr(bts.models, name),
            "queryset": getattr(bts.models, name).objects.all().order_by("id"),
            "serializer_class": getattr(bts.serializers, f"{name}Serializer"),
            "permission_classes": [permissions.IsAuthenticated],
            "pagination_class": PageNumberPaginationLarge,
        },
    )
    globals()[generated_class.__name__] = generated_class
