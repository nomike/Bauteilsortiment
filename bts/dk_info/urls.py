from django.urls import path
import inspect
from dk_info.templatetags.view_extras import snake_case
from django.db import models
import dk_info.models


from . import views

urlpatterns = []
for name in [obj.__name__ for name, obj in dk_info.models.__dict__.items()
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

    # hello world example
    urlpatterns.append(path(f'hello', views.hello,
                            name=f"hello"))


urlpatterns.extend([
    #     path('component/<int:component_id>/update_cache',
    #          views.component_update_cache, name='component_update_cache'),
])
