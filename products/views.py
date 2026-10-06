from itertools import product
import os
from urllib import request

from Lib import urllib
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_http_methods
from .models import Product, Image
from .serializers import ImageSerializer, ProductSerializer
from App.app import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import get_object_or_404
import urllib.parse
import shutil
@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_product(request):
    if not request.content_type.startswith('multipart/form-data'):
        return Response({"error": "Content-Type must be multipart/form-data"},  status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    data = request.data
    images = request.FILES.getlist('images')
    try:
        data["price"] = float(data["price"])
    except ValueError:
        return Response({"error": "Invalid price value"},status=status.HTTP_400_BAD_REQUEST)
    product_serializer = ProductSerializer(data=data)
    if not product_serializer.is_valid():
        return Response(product_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    product = product_serializer.save()

    folder_path = os.path.join(
        settings.MEDIA_ROOT,
        'product_images',
        str(product.pk)
    )

    os.makedirs(folder_path, exist_ok=True)

    fs = FileSystemStorage(location=folder_path)

    for image in images:
        filename = fs.save(image.name, image)

        image_url = os.path.join(
            settings.MEDIA_ROOT,
            'product_images',
            str(product.pk),
            filename
        )

        Image.objects.create(
            image_url=image_url.replace("\\", "/"),
            product=product
        )

    return Response(
        {"message": "Product created successfully"},
        status=status.HTTP_201_CREATED
    )
@api_view(['GET'])
@require_http_methods(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_product_all(request):
    list_product = []
    list_images=[]
    product_json={}
    products = Product.objects.all()
    for product in products:
        product_json = {
            "id": product.pk,
            "name": product.name,
            "price": product.price,
            "subcategory": product.subcategory.name,
        }
        images = Image.objects.filter(product=product)
        for image in images:
            list_images.append(image.image_url)
        product_json["images"] = list_images
        list_product.append(product_json)
        product_json={}
        list_images=[]
    return Response({"count": len(list_product), "products": list_product}, status=status.HTTP_200_OK)
@api_view(['DELETE'])
@require_http_methods(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):

    try:
        product = Product.objects.get(pk=pk)

    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    images = Image.objects.filter(product=product)

    folder_path = os.path.join(
        settings.MEDIA_ROOT,
        'product_images',
        str(pk)
    )

    for image in images:
        name_image = image.image_url.split('/')[-1].replace("\\", "/")
        image_path = os.path.join(folder_path, name_image)

        if os.path.exists(image_path):
            os.remove(image_path)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
    try:
        images.delete()
        product.delete()

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"message": "Product deleted successfully"},status=status.HTTP_200_OK)
@api_view(['GET'])
@require_http_methods(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_product_by_id(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"},status=status.HTTP_404_NOT_FOUND)
    product_json = {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "subcategory": product.subcategory.name,
    }
    images = Image.objects.filter(product=product)
    list_images = [image.image_url for image in images]
    product_json["images"] = list_images
    return Response(product_json, status=status.HTTP_200_OK)
@api_view(['PUT'])
@require_http_methods(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_product(request, pk):

    if not request.content_type.startswith('multipart/form-data'):
        return Response(
            {"error": "Content-Type must be multipart/form-data"},
            status=status.HTTP_400_BAD_REQUEST
        )

    data = request.POST.copy()

    images_files = request.FILES.getlist('images')

    try:
        data['price'] = float(data['price'])
    except (ValueError, KeyError) as e:
        return Response(
            {"error": f"invalid data: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    product = get_object_or_404(Product, id=pk)

    product_serializer = ProductSerializer(
        product,
        data=data,
        partial=True
    )

    if not product_serializer.is_valid():
        return Response(
            product_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    product_serializer.save()

    folder_path = os.path.join(
        settings.MEDIA_ROOT,
        'product_images',
        str(pk)
    )

    os.makedirs(folder_path, exist_ok=True)

    fs = FileSystemStorage(location=folder_path)

    existing_images = Image.objects.filter(product=product)

    existing_images_urls = [
        os.path.basename(image.image_url)
        for image in existing_images
    ]

    new_images_names = [
        image_file.name
        for image_file in images_files
    ]

    for existing_image_url in existing_images_urls:

        if existing_image_url not in new_images_names:

            file_path = os.path.join(
                folder_path,
                existing_image_url
            )

            if os.path.exists(file_path):
                os.remove(file_path)

            existing_images.filter(
                image_url__endswith=existing_image_url
            ).delete()

    for image_file in images_files:

        if image_file.name not in existing_images_urls:

            filename = fs.save(
                image_file.name,
                image_file
            )

            image_url = (
                f"/media/product_images/"
                f"{product.pk}/"
                f"{urllib.parse.unquote(filename)}"
            )

            image_serializer = ImageSerializer(
                data={
                    "image_url": image_url,
                    "product": product.pk
                }
            )

            if image_serializer.is_valid():
                image_serializer.save()
            else:
                return Response(
                    image_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

    return Response(
        {"message": "Product updated successfully"},
        status=status.HTTP_200_OK
    )
@api_view(['GET'])
@require_http_methods(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_product_by_subcategory(request, pk):

    products = Product.objects.filter(subcategory__id=pk)

    serializer = ProductSerializer(products, many=True)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
from django.db.models import Q
@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_products(request):
    query = request.data.get('search', '').strip()
    if not query:
        return Response(
            {"error": "Search query is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(subcategory__name__icontains=query)
    ).distinct()
    serializer = ProductSerializer(products, many=True)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def filter_products(request):
    name = request.data.get('name', '').strip()
    min_price = request.data.get('min_price')
    max_price = request.data.get('max_price')
    category_id = request.data.get('category_id')
    subcategory_id = request.data.get('subcategory_id')
    products = Product.objects.all()
    if name:
        products = products.filter(name__icontains=name)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if category_id:
        products = products.filter(subcategory__category__id=category_id)
    if subcategory_id:
        products = products.filter(subcategory__id=subcategory_id)
    serializer = ProductSerializer(products, many=True)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )