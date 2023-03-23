
import inspect

from typing import Any, Dict
import bts.models
from django.db import models
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views import View
from bts.models import AssortmentBox, StorageUnitType, StorageUnit, StorageUnitCompartment, Merchant, ComponentType, Component, SubComponent, Category, Inventory, Purchase, PurchaseLine
from django.shortcuts import render

# Vie config
view_config = {
    AssortmentBox: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"]
    },
    StorageUnitType: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"]
    },
    StorageUnit: {
        "list_fields": ["name"],
        "list_detail_link_fields": ["name"]
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
        "list_fields": ["part_number", "component_type", "merchant"],
        "list_detail_link_fields": ["part_number"],
        "sublists": ["SubComponent"]
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
        return self.model.objects.filter(**{self.kwargs['model'].lower(): self.filter_object})


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
