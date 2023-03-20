from django.shortcuts import render
from django.http import HttpResponse
from dk_info.models import Component
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
import datetime


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
    }
    return render(request, 'Component/index.html', context)


def component_update_cache(request, component_id):
    component = get_object_or_404(Component, pk=component_id)
    component.update_cache()
    component.save()

    return HttpResponse(f"Cache updated for {component}.")
