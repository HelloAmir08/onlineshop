from django.urls import path

from onlineshop import views

urlpatterns = [
    path('', views.index, name='products'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
]
