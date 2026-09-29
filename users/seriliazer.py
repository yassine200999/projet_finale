from rest_framework import serializers
from users.models import User

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
<<<<<<<< HEAD:users/serializers.py
        fields = "__all__"
========
        fields="__all__"
class UpdateUserSerilaizer(serializers,ModelSerializer):
    model=User
    fields =['first_name','last_name','email','phone_number']
>>>>>>>> a9cfca1 (Update project):users/seriliazer.py
