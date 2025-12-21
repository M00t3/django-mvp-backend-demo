from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from django.db import connection
from django.db.utils import OperationalError
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Product
from .serializers import ProductSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(
    tags=['Products'],
    parameters=[
        OpenApiParameter(name='search', description='Search products by name', required=False, type=str),
    ],
    responses=ProductSerializer(many=True),
    summary="List or Search Products",
    description="List all products or search by name"
)
class ProductListAPIView(APIView):
    """
    API endpoint to list all products or search by name.
    """

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination


    def get(self, request):
        """
        Return a list of all products.
        Supports filtering by name via the `search` query parameter.
        """
        search_query = request.query_params.get('search', None)
        if search_query:
            products = Product.objects.filter(name__icontains=search_query)
        else:
            products = Product.objects.all()
        
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        tags=['Products'],
        request=ProductSerializer,
        responses=ProductSerializer,
        summary="Create Product",
        description="Create a new product"
    )
    def post(self, request):
        """
        Create a new product instance.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Products'])
class ProductDetailAPIView(APIView):
    """
    API endpoint to retrieve, update, or delete a specific product.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    @extend_schema(
        responses=ProductSerializer,
        summary="Retrieve Product",
        description="Retrieve a specific product"
    )
    def get(self, request, pk):
        """
        Retrieve a product by its ID.
        """
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @extend_schema(
        request=ProductSerializer,
        responses=ProductSerializer,
        summary="Update Product",
        description="Update a specific product"
    )
    def put(self, request, pk):
        """
        Update a product by its ID.
        """
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={204: None},
        summary="Delete Product",
        description="Delete a product"
    )
    def delete(self, request, pk):
        """
        Delete a product by its ID.
        """
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
