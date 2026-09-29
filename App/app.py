from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from datetime import timedelta

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = self.get_the_token_from_header(
            request.META.get('HTTP_AUTHORIZATION')
        )

        if not jwt_token:
            return None

        try:
            payload = jwt.decode(
                jwt_token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_CONF.get('ALGORITHM', 'HS256')],
                audience=settings.JWT_CONF.get('JWT_AUDIENCE', 'my_app')
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')

        user_id = payload.get('user_identifier')
        if user_id is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        if not user.is_active:
            raise AuthenticationFailed('User is inactive')

        invalidated_at = user.token_invalidated_at
        token_issued_at = payload.get('iat')
        if invalidated_at is not None and token_issued_at is not None:
            if float(token_issued_at) <= invalidated_at.timestamp():
                raise AuthenticationFailed('Token has been invalidated')

        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @staticmethod
    def get_the_token_from_header(authorization_header):
        if not authorization_header:
            return None

        parts = authorization_header.split()

        if len(parts) == 2 and parts[0].lower() == 'bearer':
            return parts[1]

        return None

    @staticmethod
    def create_jwt(user):
        now = timezone.now()
        lifetime = settings.JWT_CONF.get('TOKEN_LIFETIME_HOURS', 1)
        algorithm = settings.JWT_CONF.get('ALGORITHM', 'HS256')
        audience = settings.JWT_CONF.get('JWT_AUDIENCE', 'my_app')

        payload = {
            'user_identifier': user.id,
            'exp': int((now + timedelta(hours=lifetime)).timestamp()),
            'iat': now.timestamp(),
            'email': user.email,
            'is_active': user.is_active,
            'aud': audience
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=algorithm
        )
