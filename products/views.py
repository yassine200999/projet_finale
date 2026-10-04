import os
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Product, Image
from .serializers import ProductSerializer, ImageSerializer
from App.app import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.files.storage import FileSystemStorage, default_storage
from django.shortcuts import get_object_or_404
import urllib
import shutil
from django.conf import settings
@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_product(request):
    if not request.type(object).startswith('multipart/form-data'):
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    # exteact post data and files
    data = request.data
    images = request.FILES.getlist('images')
    try:
        data["price"] = float(data["price"])
    except ValueError:
        return Response({"error": "Invalid price value"}, status=status.HTTP_400_BAD_REQUEST)
    product_serializer = ProductSerializer(data=data)
    if not product_serializer.is_valid():
        return Response({"error": "Invalid product data"}, status=status.HTTP_400_BAD_REQUEST)
    product=product_serializer.save()
    # save images
    folder_path = os.path.join(settings.MEDIA_ROOT, 'product_images', str( product.pk))
    os.makedirs(folder_path, exist_ok=True)
    fs=FileSystemStorage(location=folder_path)
    for image in images:
        filename = fs.save(image.name, image)
        image_url = os.path.join(settings.MEDIA_ROOT, 'product_images', str(product.pk), filename)
        Image.objects.create(image_url=image_url.replace("\\", "/"), product=product)
        images_serializer = ImageSerializer(Image.objects.filter(product=product), many=True)
        if not images_serializer.is_valid():
            return Response({"error": "Invalid image data"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)