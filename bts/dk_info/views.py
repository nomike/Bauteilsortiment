
import inspect

import dk_info.models
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView
from dk_info.models import Component, ComponentType, Merchant

# Create your views here.


def component_update_cache(request, component_id):
    component = get_object_or_404(Component, pk=component_id)
    component.update_cache(force='force' in request.GET)
    component.save()

    return HttpResponseRedirect(reverse('component_details', args=(component.id,)))


class ModelListView(ListView):
    model = None
    template_name = "dk_info/model_list.html"


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
