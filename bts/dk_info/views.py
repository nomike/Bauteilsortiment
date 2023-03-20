from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from dk_info.models import Component

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def components(request):
    context = {'components': Component.objects.all()}
    return render(request, 'Components/index.html', context)


def component(request, component_id):
    component = get_object_or_404(Component, pk=component_id)

    context = {
        'component': component,
        'fields': model_to_dict(component, exclude=['id']).items()
    }

    return render(request, 'Component/index.html', context)


def component_update_cache(request, component_id):
    component = get_object_or_404(Component, pk=component_id)
    component.update_cache(force='force' in request.GET)
    component.save()

    return HttpResponseRedirect(reverse('component_details', args=(component.id,)))
