# Bauteilsortiment - An Electronic Component Archival System
# Copyright (C) 2023  nomike
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
    urlpatterns.append(path(f'm/{name}', getattr(views,  f'{name}ListView').as_view(),
                            name=f"{snake_case(name)}_list"))
    urlpatterns.append(path(f'm/{name}/', getattr(views,  f'{name}ListView').as_view(),
                            name=f"{snake_case(name)}_list"))

    # filtered list
    urlpatterns.append(path(f'm/{name}/filtered/<str:model>/<int:id>', getattr(views,  f'{name}FilteredListView').as_view(),
                            name=f"{snake_case(name)}_filtered_list"))

    # generic detail page
    urlpatterns.append(path(f'm/{name}/id/<int:pk>', getattr(views,  f'{name}DetailView').as_view(),
                            name=f"{snake_case(name)}_detail"))


urlpatterns.extend([
    path('',
         views.home_view, name='home'),
    path('select_test', views.select_test, name='select_test'),
    path('json/<str:model>', views.model_json_view, name="json_list"),
    path('json/<str:model>/<int:id>/field/<str:field>',
         views.model_json_field_view, name="json_field_view"),
    path('json/<str:model>/<str:filter_model>/<int:id>',
         views.model_json_filtered_view, name="json_list_filtered"),
    path('qr/<str:model>/<int:id>.svg',
         views.qr_code_svg, name="qr_svg"),
    path('m/StorageUnit/id/<int:id>/label.svg',
         views.storage_unit_label_svg, name="storage_unit_label_svg"),
])
