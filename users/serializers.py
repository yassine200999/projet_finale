from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User
<<<<<<< HEAD
=======


>>>>>>> 205a0c98e5903dd436e683d7105fdff927f2e0b6
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
<<<<<<< HEAD
        fields = "__all__"
class UpdateUserSerilaizer(serializers.ModelSerializer):
    model=User
    fields =['first_name','last_name','email','phone_number']

=======
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
            'is_verified',
            'is_active',
            'is_admin',
            'token_last_expired',
        ]
        read_only_fields = ['is_verified', 'is_active', 'is_admin', 'token_last_expired']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
>>>>>>> 205a0c98e5903dd436e683d7105fdff927f2e0b6
