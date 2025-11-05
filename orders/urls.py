# orders/urls.py
from django.urls import path
from .views import (
    OrderCreateView, OrderListView, OrderDetailView,
    AllOrdersView, OrderStatusUpdateView
)

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    
    # Admin only
    path('all/', AllOrdersView.as_view(), name='all-orders'),
    path('<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
]