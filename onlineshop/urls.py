from django.contrib import admin
from django.urls import path

from onlineshop import views

urlpatterns = [
    path('', views.index, name='products'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('category_detail/<int:category_id>/', views.index, name='products_of_category'),
    path('order_detail/<int:pk>/save/', views.order_detail, name='order_detail'),
    path('comment_detail/<int:pk>/save/', views.comment_detail, name='comment_detail'),
    path('create_product/', views.create_product, name='create_product'),
    path('edit_product/<int:pk>/', views.product_edit, name='product_edit'),
    path('delete_product/<int:pk>/', views.product_delete, name='product_delete'),
]