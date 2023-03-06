from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path('getAllProduct/', views.getAllProductAPI.as_view(),name='getAllProduct'),
    path('getProductType/', views.getProductTypeAPI.as_view(),name='getProductType'),
    path('getAll/<str:type>', views.getAllAPI.as_view(),name='get_All'),
    path('getProductDetail/<int:id>',views.getProductDetailAPI.as_view(),name='getProduct'),
]