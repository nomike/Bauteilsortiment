
import inspect

from typing import Any
import dk_info.models
from django.db import models
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views import View
from dk_info.models import Component

# Create your views here.


def component_update_cache(request, component_id):
    component = get_object_or_404(Component, pk=component_id)
    component.update_cache(force='force' in request.GET)
    component.save()

    return HttpResponseRedirect(reverse('component_details', args=(component.id,)))


def hello(request):
    return HttpResponse("<strong>Hello</strong> world!<br/>")


class ModelListView(ListView):
    model = None
    template_name = "dk_info/model_list_page.html"


class ModelFilteredListView(ListView):
    model = None
    template_name = "dk_info/model_list_snippet.html"

    def get_queryset(self) -> QuerySet[Any]:
        print("@@@@@@@@")
        self.filter_object = get_object_or_404(
            getattr(dk_info.models, self.kwargs['model']), pk=self.kwargs['id']
        )
        return self.model.objects.filter(**{self.kwargs['model'].lower(): self.filter_object})


class ModelDetailView(DetailView):
    model = None
    template_name = "dk_info/model_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['fields'] = self.model._meta.fields
        return context


for name in [obj.__name__ for name, obj in dk_info.models.__dict__.items()
             if inspect.isclass(obj) and issubclass(obj, models.Model)]:
    generated_class = type(name + 'DetailView', (ModelDetailView, ), {
        "model": getattr(dk_info.models, name)
    })
    globals()[generated_class.__name__] = generated_class
    generated_class = type(name + 'ListView', (ModelListView, ), {
        "model": getattr(dk_info.models, name)
    })
    globals()[generated_class.__name__] = generated_class
    generated_class = type(name + 'FilteredListView', (ModelFilteredListView, ), {
        "model": getattr(dk_info.models, name)
    })
    globals()[generated_class.__name__] = generated_class
