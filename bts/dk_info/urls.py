from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('component/<str:dk_part_number>',
         views.component, name='component_details'),
    path('digikeycomponent/<str:dk_part_number>/update_cache',
         views.digikey_component_update_cache, name='digikey_component_update_cache'),
    path('component/', views.components, name='components'),
]
