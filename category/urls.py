from django.urls import path
from . import views
urlpatterns = [
path('get_all_categories',views.get_all_categories,name="get_all_categories")
]