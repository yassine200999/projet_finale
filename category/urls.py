from django.urls import path
from . import views
urlpatterns = [
path('get_all_categories',views.get_all_categories,name="get_all_categories"),
path('create_category',views.create_category,name="create_category"),
path('update_category/<int:pk>/', views.update_category, name='update_category'),
path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
path('get_SubCategory_all',views.get_SubCategory_all,name="get_SubCategory_all"),
path('get_SubCategory/<int:pk>/', views.get_SubCategory, name='get_SubCategory'),
path('create_SubCategory',views.create_SubCategory,name="create_SubCategory"),
path('update_SubCategory/<int:pk>/', views.update_SubCategory, name='update_SubCategory'),
path('delete_SubCategory/<int:pk>/', views.delete_SubCategory, name='delete_SubCategory'),
]