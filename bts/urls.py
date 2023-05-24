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
from bts.templatetags.view_extras import snake_case

from . import views

urlpatterns = []

# generate urls for all models
for object in [
    object
    for name, object in bts.models.__dict__.items()
    if inspect.isclass(object) and issubclass(object, models.Model)
]:
    # generic list
    urlpatterns.append(
        path(
            f"m/{object._meta.object_name}",
            getattr(views, f"{object._meta.object_name}ListView").as_view(),
            name=f"{object._meta.object_name}",
        )
    )
    urlpatterns.append(
        path(
            f"m/{object._meta.object_name}/",
            getattr(views, f"{object._meta.object_name}ListView").as_view(),
            name=f"{object._meta.object_name}_list",
        )
    )

    # filtered list
    urlpatterns.append(
        path(
            f"m/{object._meta.object_name}/filtered/<str:field>/<str:value>",
            getattr(views, f"{object._meta.object_name}FilteredListView").as_view(),
            name=f"{object._meta.object_name}_filtered_list",
        )
    )

    # generic detail page
    urlpatterns.append(
        path(
            f"m/{object._meta.object_name}/id/<int:pk>",
            getattr(views, f"{object._meta.object_name}DetailView").as_view(),
            name=f"{object._meta.object_name}_detail",
        )
    )

# add specific views
urlpatterns.extend(
    [
        path("", views.home_view, name="home"),
        path("json/<str:model>", views.model_json_view, name="json_list"),
        path(
            "json/<str:model>/<int:id>/field/<str:field>",
            views.model_json_field_view,
            name="json_field_view",
        ),
        path(
            "json/<str:model>/<str:field>/<str:value>",
            views.model_json_filtered_view,
            name="json_list_filtered",
        ),
        path("qr/<str:model>/<int:id>.svg", views.qr_code_svg, name="qr_svg"),
        path("qrr/<int:id>", views.qr_redirect, name="qr_redirect"),
        path("labels/<int:id>", views.labelpage, name="qr_svg"),
    ]
)

# rest views
router = routers.DefaultRouter()
router.register(r"api/v1/merchant", views.MerchantViewSet)
router.register(r"api/v1/location", views.LocationViewSet)
router.register(r"api/v1/assortmentboxes", views.AssortmentBoxViewSet)

urlpatterns.extend(
    [
        path('', include(router.urls)),
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    ]
)
