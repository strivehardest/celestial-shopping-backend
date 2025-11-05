# store/views.py
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, ProductListSerializer, 
    ProductDetailSerializer, ProductCreateUpdateSerializer,
    ReviewSerializer
)

class CategoryListView(generics.ListCreateAPIView):
    """
    GET /api/store/categories/
    POST /api/store/categories/ (admin only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

class ProductListView(generics.ListAPIView):
    """
    GET /api/store/products/
    List all products with filtering and search
    """
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

class ProductDetailView(generics.RetrieveAPIView):
    """
    GET /api/store/products/{slug}/
    Get product details
    """
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class ProductCreateView(generics.CreateAPIView):
    """
    POST /api/store/products/create/
    Create new product (admin only)
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAdminUser]

class ProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/DELETE /api/store/products/{id}/manage/
    Update or delete product (admin only)
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAdminUser]

class ReviewCreateView(generics.CreateAPIView):
    """
    POST /api/store/products/{product_id}/reviews/
    Create a review for a product
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(id=product_id)
        serializer.save(user=self.request.user, product=product)