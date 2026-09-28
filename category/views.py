from django.views.decorators.http import require_http_methods
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from App.app import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_categories(request):
    categories=Category.objects.all()
    serializer=CategorySerializer(categories,many=True)
    return Response(serializer.data)
