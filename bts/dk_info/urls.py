from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('component/<str:dk_part_number>', views.component, name='component_details'),
    path('component/<str:dk_part_number>/update_cache', views.update_cache, name='component_update_cache'),
    path('component/', views.components, name='components'),
]
