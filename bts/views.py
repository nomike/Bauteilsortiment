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

import qrcode
import qrcode.image.svg
import drawsvg
from django.db import models
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

import bts.models
from bts.models import (AssortmentBox, Category, Component, ComponentType,
                        Inventory, Merchant, Purchase, PurchaseLine,
                        StorageUnit, StorageUnitCompartment, StorageUnitType,
                        SubComponent)
from bts.templatetags import view_extras


# Vie config
view_config = {
    AssortmentBox: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"],
        "sublists": ["StorageUnit"]
    },
    StorageUnitType: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"]
    },
    StorageUnit: {
        "list_fields": ["number", "assortment_box"],
        "list_detail_link_fields": ["number"],
        "sublists": ["StorageUnitCompartment"]
    },
    StorageUnitCompartment: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"],
        "sublists": ["Inventory"]
    },
    Merchant: {
        "list_fields": ["name", "url"],
        "list_detail_link_fields": ["name"],
        "sublists": ["Component", "Purchase"]
    },
    ComponentType: {
        "list_fields": ["name", "parent"],
        "list_detail_link_fields": ["name"],
        "sublists": ["SubComponent"]
    },
    Component: {
        "list_fields": ["part_number", "product_description", "merchant"],
        "list_detail_link_fields": ["part_number"],
        "sublists": ["SubComponent", "PurchaseLine"]
    },
    SubComponent: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"]
    },
    Category: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"]
    },
    Inventory: {
        "list_fields": ["id", "sub_component", "storage_unit_compartment", "timestamp", "count"],
        "list_detail_link_fields": ["id"]
    },
    Purchase: {
        "list_fields": ["order_number", "merchant", "timestamp"],
        "list_detail_link_fields": ["order_number"],
        "sublists": ["PurchaseLine"]
    },
    PurchaseLine: {
        "list_fields": ["id", "component", "quantity", "unit_price", "purchase"],
        "list_detail_link_fields": ["id"]
    },
}

# Create your views here.


def home_view(request):
    context = {
        "types": view_config.keys()
    }
    return render(request, 'bts/home.html', context)


# def component_update_cache(request, component_id):
#     component = get_object_or_404(Component, pk=component_id)
#     component.update_cache(force='force' in request.GET)
#     component.save()

#     return HttpResponseRedirect(reverse('component_details', args=(component.id,)))


class ConfiguredListView(ListView):
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        for key, value in view_config[self.model].items():
            context_data[key] = value
        return context_data


class ConfiguredDetailView(DetailView):
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        for key, value in view_config[self.model].items():
            context_data[key] = value
        return context_data


def model_json_view(request, model: str):
    return JsonResponse(list(getattr(bts.models, model).objects.values()), safe=False)


def model_json_filtered_view(View, model: str, filter_model: str, id: int):
    data = getattr(bts.models, model).objects.filter(
        **{view_extras.snake_case(filter_model): id})
    return JsonResponse(list(data.values()), safe=False)


def model_json_field_view(request, model: str, id: int, field: str):
    return JsonResponse(getattr(get_object_or_404(getattr(bts.models, model), pk=id), field), safe=False)


def select_test(request):
    return render(request, template_name='bts/select_test.html')


class ModelListView(ConfiguredListView):
    model = None
    template_name = "bts/model_list_page.html"


class ModelFilteredListView(ConfiguredListView):
    model = None
    template_name = "bts/model_list_snippet.html"

    def get_queryset(self) -> QuerySet[Any]:
        self.filter_object = get_object_or_404(
            getattr(bts.models, self.kwargs['model']), pk=self.kwargs['id']
        )
        return self.model.objects.filter(**{view_extras.snake_case(self.kwargs['model']): self.filter_object})


class ModelDetailView(ConfiguredDetailView):
    model = None
    template_name = "bts/model_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['fields'] = self.model._meta.fields
        return context


def storage_unit_label_svg(request, id):
    su = get_object_or_404(StorageUnit, pk=id)
    sucs = StorageUnitCompartment.objects.filter(storage_unit=su)
    print("ffffooo")
    print(sucs[1].name)  # .name)
    d = drawsvg.Drawing(2000, 1000, origin='top-left')
    r = drawsvg.Rectangle(0, 0, "50mm", "10mm", fill='#00000000',
                          stroke="#000000", stroke_witdth="hairline")
    img = qrcode.make(request.build_absolute_uri(reverse(f'storage_unit_detail', args=[id])),
                      image_factory=qrcode.image.svg.SvgFragmentImage,
                      box_size=4)

    d.append(drawsvg.Image("1", "1", "10mm", "10mm",
             data=img.to_string(encoding='unicode').encode('utf-8'), embed=False, mime_type="image/svg+xml"))
    r.append_title("Our first rectangle")  # Add a tooltip
    d.append(r)
    d.append(drawsvg.Line(40,  20, 180, 20, fill='red',
                          stroke="#000000", stroke_witdth=20))

    tt = "foo"
    bt = "bar"
    if len(sucs) >= 1:
        tt = Inventory.objects.filter(storage_unit_compartment=sucs[0])[
            0].sub_component.name
    elif len(sucs) >= 2:
        bt = Inventory.objects.filter(storage_unit_compartment=sucs[1])[
            0].sub_component.name

    top_text = drawsvg.Text(tt, 8, x=40,
                            y=13, font_family="arial, sans-serif")
    bottom_text = drawsvg.Text(
        bt, 8, x=40, y=30, font_family="arial, sans-serif")
    d.append(top_text)
    d.append(bottom_text)
    return HttpResponse(d.as_svg(), content_type="image/svg+xml")


def qr_code_svg(request, model, id):
    box_size = request.GET.get('box_size')

    img = qrcode.make(request.build_absolute_uri(reverse(f'merchant_detail', args=[id])),
                      image_factory=qrcode.image.svg.SvgImage,
                      box_size=box_size or 4)

    return HttpResponse(img.to_string(encoding='unicode'), content_type="image/svg+xml")


for name in [obj.__name__ for name, obj in bts.models.__dict__.items()
             if inspect.isclass(obj) and issubclass(obj, models.Model)]:
    generated_class = type(name + 'DetailView', (ModelDetailView, ), {
        "model": getattr(bts.models, name)
    })
    globals()[generated_class.__name__] = generated_class
    generated_class = type(name + 'ListView', (ModelListView, ), {
        "model": getattr(bts.models, name)
    })
    globals()[generated_class.__name__] = generated_class
    generated_class = type(name + 'FilteredListView', (ModelFilteredListView, ), {
        "model": getattr(bts.models, name)
    })
    globals()[generated_class.__name__] = generated_class
