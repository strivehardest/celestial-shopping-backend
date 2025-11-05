# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from store.serializers import ProductListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for viewing orders"""
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'full_name', 'email', 
            'phone', 'address', 'city', 'total_amount', 'status',
            'payment_status', 'transaction_id', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['order_number', 'user']

class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders"""
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone', 'address', 'city',
            'payment_method', 'items'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calculate total
        total = sum(item['price'] * item['quantity'] for item in items_data)
        
        # Create order
        order = Order.objects.create(
            user=self.context['request'].user,
            total_amount=total,
            **validated_data
        )
        
        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating order status (admin)"""
    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'transaction_id']