from django.contrib import admin
from django.urls import path

from onlineshop import views

urlpatterns = [
    path('', views.index, name='products'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('category-detail/<int:category_id>/', views.index, name='products_of_category'),
    path('order-detail/<int:pk>/save/', views.order_detail, name='order_detail'),
    path('comment-detail/<int:pk>/save/', views.comment_detail, name='comment_detail'),
]