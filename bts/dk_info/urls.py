from django.urls import path

from . import views

urlpatterns = [
    path('generic/Component', views.ComponentListView.as_view(),
         name="component_list"),
    path('generic/Merchant', views.MerchantListView.as_view(),
         name="merchant_list"),
    path('generic/Component/<int:pk>', views.ComponentDetailView.as_view(),
         name="component_detail"),
    path('generic/Merchant/<int:pk>', views.MerchantDetailView.as_view(),
         name="merchant_detail"),
    path('generic/ComponentType', views.ComponentTypeListView.as_view(),
         name="component_type_list"),
    path('generic/ComponentType/<int:pk>', views.ComponentTypeDetailView.as_view(),
         name="component_type_detail"),
    #     path('component/<int:component_id>/update_cache',
    #          views.component_update_cache, name='component_update_cache'),
]
