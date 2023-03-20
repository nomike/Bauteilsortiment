
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView
from dk_info.models import Component

# Create your views here.


def component_update_cache(request, component_id):
    component = get_object_or_404(Component, pk=component_id)
    component.update_cache(force='force' in request.GET)
    component.save()

    return HttpResponseRedirect(reverse('component_details', args=(component.id,)))


class ComponentListView(ListView):
    model = Component
    context_object_name = "all_components"


class ComponentDetailView(DetailView):
    model = Component
    context_object_name = "all_components"

    def get_queryset(self):
        self.component = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return Component.objects.filter(pk=self.component.pk)
