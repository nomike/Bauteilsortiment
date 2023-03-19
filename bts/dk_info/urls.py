from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('component/', views.components, name='components'),
    path('component/<str:part_number>',
         views.component, name='component_details'),
    path('digikeycomponent/', views.components, name='digikeycomponents'),
    path('digikeycomponent/<str:part_number>',
         views.component, name='digikeycomponent_details'),
    path('component/<str:part_number>/update_cache',
         views.digikey_component_update_cache, name='component_update_cache'),
]
