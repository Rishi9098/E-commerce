from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name = 'product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/product/add/', views.product_add, name='product_add'),
    path('seller/product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('seller/product/<int:pk>/delete/', views.product_delete, name='product_delete'),
]