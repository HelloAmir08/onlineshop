from django.urls import path
from onlineshop import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category_detail/<int:category_id>/', views.ProductListView.as_view(), name='products_of_category'),
    path('order_detail/<int:pk>/save/', views.OrderCreateView.as_view(), name='order_detail'),
    path('comment_detail/<int:pk>/save/', views.CommentCreateView.as_view(), name='comment_detail'),
    path('create_product/', views.ProductCreateView.as_view(), name='create_product'),
    path('edit_product/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('delete_product/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
]
