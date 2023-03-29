import inspect

from django.db import models
from django.urls import path

import bts.models
from bts.templatetags.view_extras import snake_case

from . import views

urlpatterns = []
for name in [obj.__name__ for name, obj in bts.models.__dict__.items()
             if inspect.isclass(obj) and issubclass(obj, models.Model)]:
    # generic list
    urlpatterns.append(path(f'generic/{name}', getattr(views,  f'{name}ListView').as_view(),
                            name=f"{snake_case(name)}_list"))
    urlpatterns.append(path(f'generic/{name}/', getattr(views,  f'{name}ListView').as_view(),
                            name=f"{snake_case(name)}_list"))

    # filtered list
    urlpatterns.append(path(f'generic/{name}/filtered/<str:model>/<int:id>', getattr(views,  f'{name}FilteredListView').as_view(),
                            name=f"{snake_case(name)}_filtered_list"))

    # generic detail page
    urlpatterns.append(path(f'generic/{name}/id/<int:pk>', getattr(views,  f'{name}DetailView').as_view(),
                            name=f"{snake_case(name)}_detail"))


urlpatterns.extend([
    path('',
         views.home_view, name='home'),
    path('select_test', views.select_test, name='select_test'),
    path('json/<str:model>', views.model_json_view, name="json_list"),
    path('json/<str:model>/<str:filter_model>/<int:id>',
         views.model_json_filtered_view, name="json_list_filtered"),
])
