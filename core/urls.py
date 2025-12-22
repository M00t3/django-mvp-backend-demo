from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView, HealthCheckAPIView
from .auth_views import RegisterAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('health/', HealthCheckAPIView.as_view(), name='health-check'),
]
