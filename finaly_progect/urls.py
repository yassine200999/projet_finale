"""
URL configuration for finaly_progect project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from products.views import init_category_subcategory

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include('App.urls')),
    path("category/", include('category.urls')),
    path("users/", include("users.urls")),
    path("products/", include("products.urls")),
    path(
        "init_category_subcategory/",
        init_category_subcategory,
        name="init_category_subcategory_root",
    ),
]
