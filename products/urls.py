from django.urls import path
from products import views

urlpatterns = [
    path('create_product/', views.create_product, name='create_product'),
    path('get_all_products/', views.get_all_products, name='get_all_products'),
    path('get_product/<int:pk>/', views.get_product, name='get_product'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
       path(
        'init_category_subcategory/',
        views.init_category_subcategory,
        name='init_category_subcategory'
    ),
]
