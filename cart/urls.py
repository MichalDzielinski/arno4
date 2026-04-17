from django.urls import path
from . import views

urlpatterns = [
   
    path('cart_summary/', views.cart_summary, name='cart summary'),
    path('cart_add/', views.cart_add, name='cart add'),
    path('cart_delete/', views.cart_delete, name='cart delete'),
    path('cart_update/', views.cart_update, name='cart update'),
]