from django.urls import path
from products import views
urlpatterns = [
    path('create_product/', views.create_product, name='create_product'),
    path('get_product_all/', views.get_product_all, name='get_product_all'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('get_product_by_id/<int:pk>/', views.get_product_by_id, name='get_product_by_id'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
        path(
        'get_product_by_subcategory/<int:pk>/',
        views.get_product_by_subcategory,
        name='get_product_by_subcategory'
    ),
    path('search_products/', views.search_products, name='search_products'),
    path('filter_products/', views.filter_products, name='filter_products')
    ]
