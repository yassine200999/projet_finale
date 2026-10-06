import os
import shutil

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Image
from .serializers import ProductSerializer, ImageSerializer
from App.app import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_product(request):
    if not request.content_type.startswith('multipart/form-data'):
        return Response(
            {"error": "Content-Type must be multipart/form-data"},
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )

    data = request.data.copy()
    images = request.FILES.getlist('images')

    price = data.get('price')
    if price is None:
        return Response(
            {"error": "Price is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        data['price'] = float(price)
    except (TypeError, ValueError):
        return Response(
            {"error": "Invalid price value"},
            status=status.HTTP_400_BAD_REQUEST
        )

    product_serializer = ProductSerializer(data=data)
    if not product_serializer.is_valid():
        return Response(
            product_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

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
        ).replace("\\", "/")

        Image.objects.create(
            image_url=image_url,
            product=product
        )

    return Response(
        ProductSerializer(product).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_products(request):
    products = Product.objects.prefetch_related(
        'images',
        'subcategory'
    ).all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_product(request, pk):
    try:
        product = Product.objects.prefetch_related(
            'images',
            'subcategory'
        ).get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(
        ProductSerializer(product).data,
        status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
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

    for image in images:
        if image.image_url:
            file_path = image.image_url
            if not os.path.isabs(file_path):
                file_path = os.path.join(settings.BASE_DIR, file_path)

            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    pass

    images.delete()
    product.delete()

    folder_path = os.path.join(
        settings.MEDIA_ROOT,
        'product_images',
        str(pk)
    )

    if os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
        except OSError:
            pass

    return Response(
        {"message": "Product deleted successfully"},
        status=status.HTTP_200_OK
    )
