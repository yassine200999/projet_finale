from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
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
