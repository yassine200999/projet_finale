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
    serializer = ObtainTokenSerializer(data=request.data)

    if not serializer.is_valid():
        return JsonResponse({"error": serializer.errors}, status=400)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    user = User.objects.filter(email=email).first()

    if user is None:
        return JsonResponse({"error": "Invalid email or password"}, status=401)

    user_auth = authenticate(request, username=email, password=password)

    if user_auth is None:
        return JsonResponse({"error": "Invalid email or password"}, status=401)

    if not user.is_verified:
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
    user.save(update_fields=['token_last_expired'])

    return JsonResponse({
        "message": "login successfully",
        "token": jwt_token,
        "CurrentUser": current_user
    }, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    logout(request)
    cache.delete('CurrentUser')
    return JsonResponse({"message": "logout successfully"}, status=200)
