from users.models import User
from rest_framwork.reponse import Reponse
from users.serilaizers import SignUpSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decrators import api_view, permission_classes,authentication_classes
from django.views.decrators.http import require_http_methods
from rest_framework import status
from authentication.athentication import JWTAthentication
from django.core import serializers
import json
@api_view(['POST'])
@require_http_methods(['POST'])
@permission_classes([AllowAny])
#@authentication_classes([JWTAthentication])
# @permission_classes([IsAuthenticated])
def add_user(request):
    data=request.data
    data['password']=make_password(data['password'])
    sigin_up_serializer= SignUpSerializer(data=data)
    if sigin_up_serializer.is_vaild():
        sigin_up_serializer.save()