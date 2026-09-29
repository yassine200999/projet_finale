from django.urls import path
from . import views

urlpatterns = [
    path("add_user", views.add_user, name="add_user"),
    path("update_user/<int:pk>", views.update_user, name="update_user")
]
