import json
from datetime import timedelta
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .app import JWTAuthentication
from .serializers import ObtainTokenSerializer
User = get_user_model()
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    data = json.loads(request.body)
    serializer = ObtainTokenSerializer(data=data)
    if serializer.is_valid():
        user = User.objects.filter(email=data['email']).first()
        user_auth = authenticate(
            request,
            username=data['email'],
            password=data['password']
        )
        if user and user_auth and not user.is_verified:
            current_user = {
                "id": user.id,
                "username": user.first_name,
                "email": user.email,
                "is_verified": user.is_verified,
                "is_admin": user.is_admin
            }
            return JsonResponse({
                "error": "user is not verified",
                "CurrentUser": current_user
            }, status=400)
        if user_auth:
            login(request, user)
            jwt_token = str(JWTAuthentication.create_jwt(user))
            current_user = {
                "id": user.pk,
                "username": user.first_name,
                "email": user.email,
                "is_verified": user.is_verified,
                "is_admin": user.is_admin
            }
            cache.set('CurrentUser', current_user)

            user.token_last_expired = timezone.now() + timedelta(
                hours=settings.JWT_CONF['TOKEN_LIFETIME_HOURS']
            )
            user.save()

            return JsonResponse({
                "message": "login successfully",
                "token": jwt_token,
                "CurrentUser": current_user
            }, status=200)

        return JsonResponse({
            "error": "Invalid email or password"
        }, status=401)

    return JsonResponse({
        "error": serializer.errors
    }, status=400)
@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        logout(request)

        return JsonResponse({
            "message": "logout successfully"
        }, status=200)

    except AttributeError:
        return JsonResponse({
            "error": "user not found"
        }, status=400)
