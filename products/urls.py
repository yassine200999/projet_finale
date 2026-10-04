from django.urls import path
from products import views
urlpatterns = [
    path('create_product/', views.create_product, name='create_product'),
]