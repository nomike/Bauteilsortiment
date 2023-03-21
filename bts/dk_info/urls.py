from django.urls import path
import inspect
from dk_info.templatetags.view_extras import snake_case
from django.db import models
import dk_info.models


from . import views

urlpatterns = []
for name in [obj.__name__ for name, obj in dk_info.models.__dict__.items()
             if inspect.isclass(obj) and issubclass(obj, models.Model)]:
    urlpatterns.append(path(f'generic/{name}', getattr(views,  f'{name}ListView').as_view(),
                            name=f"{snake_case(name)}_list"))
    urlpatterns.append(path(f'generic/{name}/', getattr(views,  f'{name}ListView').as_view(),
                            name=f"{snake_case(name)}_list"))
    urlpatterns.append(path(f'generic/{name}/<int:pk>', getattr(views,  f'{name}DetailView').as_view(),
                            name=f"{snake_case(name)}_detail"))


urlpatterns.extend([
    #     path('component/<int:component_id>/update_cache',
    #          views.component_update_cache, name='component_update_cache'),
])
