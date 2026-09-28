from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from datetime import datetime, timedelta

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
                algorithms=["HS256"],
                audience=settings.JWT_CONF['JWT_AUDIENCE']
            )

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')

        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')

        user_id = payload.get('user_identifier')

        if user_id is None:
            raise AuthenticationFailed(
                'User identifier not found in JWT'
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        if not user.is_active:
            raise AuthenticationFailed('User is inactive')

        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @staticmethod
    def get_the_token_from_header(authorization_header):
        if (
            authorization_header
            and authorization_header.lower().startswith('bearer ')
        ):
            return authorization_header.split(' ', 1)[1].strip()

        return None

@staticmethod
def create_jwt(user):
    now = timezone.now()
    payload = {
        "user_identifier": user.id,
        "exp": int((now + timedelta(
            hours=settings.JWT_CONF['TOKEN_LIFETIME_HOURS']
        )).timestamp()),
        "iat": int(now.timestamp()),
        "email": user.email,
        "is_active": user.is_active,
        "aud": settings.JWT_CONF.get("JWT_AUDIENCE", "my_app")
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    