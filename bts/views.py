
import inspect
import json
from typing import Any, Dict

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
        "list_detail_link_fields": ["name"]
    },
    Merchant: {
        "list_fields": ["name", "url"],
        "list_detail_link_fields": ["name"],
        "sublists": ["Component", "Purchase"]
    },
    ComponentType: {
        "list_fields": ["name", "parent"],
        "list_detail_link_fields": ["name"]
    },
    Component: {
        "list_fields": ["part_number",  "merchant"],
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
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"]
    },
    Purchase: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"]
    },
    PurchaseLine: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"]
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
