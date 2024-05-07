from django.urls import path
from .views import (
    ProductListCreate,
    ProductUpdate,
    ProductDestroy,
    CategoryListCreate,
    CategoryUpdate,
    CategoryDestroy,
)

urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductUpdate.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDestroy.as_view(), name='product-destroy'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryUpdate.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDestroy.as_view(), name='category-destroy'),
]

