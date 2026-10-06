from django.urls import path
from . import views

urlpatterns = [
    path("add_user/", views.add_user, name="add_user"),
    path("update_user/<int:pk>/", views.update_user, name="update_user"),
    path("toogle_user/<int:user_id>/", views.toogle_user, name="toogle_user"),
    path("change_password/<int:user_id>/", views.change_password, name="change_password"),
]
