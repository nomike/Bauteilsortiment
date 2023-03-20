from django.urls import path

from . import views

urlpatterns = [
    path('generic/Component', views.ComponentListView.as_view(),
         name="component_list"),
    path('generic/Component/<int:pk>', views.ComponentDetailView.as_view(),
         name="component_detail"),
    #     path('component/<int:component_id>/update_cache',
    #          views.component_update_cache, name='component_update_cache'),
]
