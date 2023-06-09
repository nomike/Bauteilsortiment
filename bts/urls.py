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
from django.urls import include, path
from rest_framework import routers

import bts.models


from . import views

urlpatterns = []
router = routers.DefaultRouter()

# generate urls for all models
for object in [
    object
    for name, object in bts.models.__dict__.items()
    if inspect.isclass(object) and issubclass(object, models.Model)
]:
    urlpatterns.extend(
        (
            path(
                f"m/{object._meta.object_name}",
                getattr(views, f"{object._meta.object_name}ListView").as_view(),
                name=f"{object._meta.object_name}",
            ),
            path(
                f"m/{object._meta.object_name}/",
                getattr(views, f"{object._meta.object_name}ListView").as_view(),
                name=f"{object._meta.object_name}_list",
            ),
            path(
                f"m/{object._meta.object_name}/filtered/<str:field>/<str:value>",
                getattr(views, f"{object._meta.object_name}FilteredListView").as_view(),
                name=f"{object._meta.object_name}_filtered_list",
            ),
            path(
                f"m/{object._meta.object_name}/id/<int:pk>",
                getattr(views, f"{object._meta.object_name}DetailView").as_view(),
                name=f"{object._meta.object_name}_detail",
            ),
        )
    )
    # restfraemwork api
    router.register(
        r"api/v0/" + object._meta.verbose_name_plural.title().replace(" ", ""),
        getattr(views, f"{object._meta.object_name}ViewSet"),
    )

urlpatterns.extend(
    [
        path("", views.home_view, name="home"),
        path("qr/<str:model>/<int:id>.svg", views.qr_code_svg, name="qr_svg"),
        path("qrr/<int:id>", views.qr_redirect, name="qr_redirect"),
        path("labels/<int:id>", views.labelpage, name="labelpage"),
        path("", include(router.urls)),
        path(
            "api-auth/",
            include("rest_framework.urls", namespace="rest_framework"),
        ),
    ]
)
