# store/serializers.py
from rest_framework import serializers
from .models import Category, Product, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories"""
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'product_count']
    
    def get_product_count(self, obj):
        return obj.products.filter(available=True).count()

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for product reviews"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product listing (less detail)"""
    category = serializers.StringRelatedField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'image', 'stock', 'in_stock', 'category']

class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product details (full info)"""
    category = CategorySerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'image', 
            'stock', 'in_stock', 'available', 'category', 
            'reviews', 'average_rating', 'review_count',
            'created_at', 'updated_at'
        ]
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0
    
    def get_review_count(self, obj):
        return obj.reviews.count()

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products (admin)"""
    class Meta:
        model = Product
        fields = '__all__'