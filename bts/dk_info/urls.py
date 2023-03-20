from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('component/', views.components, name='components'),
    path('component/<int:component_id>',
         views.component, name='component_details'),
    path('component/<int:component_id>/update_cache',
         views.component_update_cache, name='component_update_cache'),
]
