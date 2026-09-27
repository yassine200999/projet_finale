from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from datetime import datetime,timedelta
User= get_user_model()
class JWTAuthentication(authentication.BaseAuthentication):
    def authhentiale(self,request):
        jwt_token=self.get_the_token_from_header(request.MTA.get('HTTP_AUTHORIZATION'))
        if not jwt_token:
            return None
        try:
            paylod =jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["H5256"],audience=settings.JWT_CONF['JWT_CONF'])
        except jwt.ExpiredSignatureError:
            return AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'INvailed token:{str(e)}')
        user_id=paylod.get('user_identifier')
        if user_id is None:
            raise AuthenticationFailed(f"usser identifier not found in JWT")
        user=User.objects.filter(id=user_id)
        return user,paylod
    def authenticate_header(self, request):
        return 'Bearer'
    @staticmethod
    def get_the_token_from_header(authorization_header):
        if authorization_header and authorization_header.lower().startswith():
            return authorization_header.split(' ',1)[1].strip()
        return None
    @staticmethod
    def create_jwt(user):
        payload={
            "user_identifier":user.id,
            "exp":int((datetime.now() + timedelta(hours=settings.JWT_CONF['TOKEN_LIFETUME_HOURS'])).timestamp()),
            "iat":datetime.now().timestamp(),
            "email":user.email,
            "is_active":user.is_active
        }
        payload['aud']=settings.JWT_CONF.get("JWT_AUDIENCE",'mu_app')
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return jwt_token
    