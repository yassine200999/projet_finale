from django.views.decorators.http import require_http_methods
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from App.app import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
@api_view(['GET'])
@require_http_methods(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_categories(request):
    categories=Category.objects.all()
    serializer=CategorySerializer(categories,many=True)
    return Response(serializer.data)
    # return JsonResponse({"data":serializer.data}) 
@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def creat_catygorie(request):
    data = request.data
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
