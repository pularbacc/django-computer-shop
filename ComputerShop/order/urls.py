from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
      path('addToCart/<int:id_product>', views.addToCartAPI.as_view(),name='addItem'),
      path('getCartItems/', views.getCartItemsAPI.as_view(),name='getItems'),
      path('removeFromCart/', views.removeFromCart.as_view(),name='removeItem'),
      path('getOrders/', views.getOrdersAPI.as_view(),name='getOrders'),
      path('getOrderDetail/<int:id_order>', views.getOrderDetailAPI.as_view(),name='getOrderDetail'),
      path('makeOrder/', views.addNewOrderAPI.as_view(),name='makeAnOrder'),
]