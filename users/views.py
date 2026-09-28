from users.models import User
from rest_framework.response import Response
from users.serializers import SignUpSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.http import require_http_methods
from rest_framework import status
from authentication.authentication import JWTAuthentication
from django.core import serializers
import json
@api_view(['POST'])
@require_http_methods(['POST'])
@permission_classes([AllowAny])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def add_user(request):
    data = request.data.copy()
    data['password'] = make_password(data['password'])
    signin_up_serializer = SignUpSerializer(data=data)
    if signin_up_serializer.is_valid():
        signin_up_serializer.save()
        return Response( {'message': 'account created'}, status=status.HTTP_201_CREATED)
    return Response(signin_up_serializer.errors,status=status.HTTP_400_BAD_REQUEST)