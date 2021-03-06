# From django
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# From drf 
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

# From w 
from products.models import Product, Category 
from products.serializers import ProductSerializer, \
    CategorySerializer, ProductReviewSerializer, ProductReviewPOSTSerializer

ONE_HOUR = 60*60

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects \
            .select_related('category') \
            .prefetch_related('reviews') \
            .prefetch_related('tags') 

    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tags', 'category']
    search_fields = ['display_name', 'description', 'category__description',
        'reviews__commentary']
    permission_classes = []

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @method_decorator(cache_page(ONE_HOUR))
    def list(self, request):
        return super().list(request)

    @action(detail=True, methods=['GET'])
    def reviews(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        reviews = product.reviews.values()
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ProductReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def new_review(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        request.data['product'] = product.pk
        serializer = ProductReviewPOSTSerializer(data=request.data)
        if not serializer.is_valid():
            return Response('body review invalido', status=status.HTTP_400_BAD_REQUEST)
        review = serializer.save()
        
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []
    
    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @method_decorator(cache_page(ONE_HOUR))
    def list(self, request):
        return super().list(request)