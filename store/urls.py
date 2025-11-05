# store/urls.py
from django.urls import path
from .views import (
    CategoryListView, ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateDeleteView, ReviewCreateView
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    
    # Products
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/manage/', ProductUpdateDeleteView.as_view(), name='product-manage'),
    
    # Reviews
    path('products/<int:product_id>/reviews/', ReviewCreateView.as_view(), name='review-create'),
]