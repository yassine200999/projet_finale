import os
import shutil
from django.views.decorators.http import require_http_methods
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
@require_http_methods(["POST"])
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
@require_http_methods(["GET"])
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
@require_http_methods(["GET"])
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
@require_http_methods(["DELETE"])
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
from django.core.management import call_command
@api_view(['POST'])
@require_http_methods(["POST"]) 
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def init_category_subcategory(request):
    try:
        call_command('init_category_subcategory')
        return Response(
            {"message": "Categories and subcategories initialized successfully","success": True},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": str(e),"success": False},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@api_view(['PUT', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductSerializer(
        product,
        data=request.data,
        partial=request.method == 'PATCH'
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

from decimal import Decimal, InvalidOperation
from django.db.models import Q
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_products(request):
    products = Product.objects.prefetch_related(
        'images',
        'subcategory'
    ).all()

    # Search by product name
    name = request.data.get('name', request.data.get('q', ''))

    if not isinstance(name, str):
        return Response(
            {"error": "Name must be a string"},
            status=status.HTTP_400_BAD_REQUEST
        )

    name = name.strip()

    if name:
        products = products.filter(name__icontains=name)

    # Filter by category
    category = request.data.get('category')

    if category not in (None, ''):
        try:
            category = int(category)
            if category <= 0:
                raise ValueError

            products = products.filter(
                subcategory__category_id=category
            )
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid category ID"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Filter by subcategory
    subcategory = request.data.get('subcategory')

    if subcategory not in (None, ''):
        try:
            subcategory = int(subcategory)
            if subcategory <= 0:
                raise ValueError

            products = products.filter(
                subcategory__id=subcategory
            )
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid subcategory ID"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Filter by minimum and maximum price
    min_price = request.data.get('min_price')
    max_price = request.data.get('max_price')

    try:
        if min_price not in (None, ''):
            min_price = Decimal(str(min_price))
            if not min_price.is_finite() or min_price < 0:
                raise InvalidOperation
            products = products.filter(price__gte=min_price)

        if max_price not in (None, ''):
            max_price = Decimal(str(max_price))
            if not max_price.is_finite() or max_price < 0:
                raise InvalidOperation
            products = products.filter(price__lte=max_price)

        if (
            min_price not in (None, '')
            and max_price not in (None, '')
            and min_price > max_price
        ):
            return Response(
                {"error": "min_price cannot exceed max_price"},
                status=status.HTTP_400_BAD_REQUEST
            )

    except (InvalidOperation, TypeError, ValueError):
        return Response(
            {"error": "Prices must be valid non-negative numbers"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Ordering
    ordering_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        'name_desc': '-name',
    }

    ordering = request.data.get('ordering', 'name_asc')

    if ordering not in ordering_options:
        return Response(
            {
                "error": "Invalid ordering",
                "allowed_values": list(ordering_options.keys())
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    products = products.order_by(
        ordering_options[ordering],
        'id'
    ).distinct()

    serializer = ProductSerializer(products, many=True)

    return Response(
        {
            "count": len(serializer.data),
            "results": serializer.data
        },
        status=status.HTTP_200_OK
    )
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def filter_products(request):
    products = Product.objects.prefetch_related(
        'images',
        'subcategory'
    ).all()

    min_price = request.data.get('minprice')
    max_price = request.data.get('maxprice')

    try:
        if min_price not in (None, ''):
            min_price = Decimal(str(min_price))
            if not min_price.is_finite() or min_price < 0:
                raise InvalidOperation
            products = products.filter(price__gte=min_price)

        if max_price not in (None, ''):
            max_price = Decimal(str(max_price))
            if not max_price.is_finite() or max_price < 0:
                raise InvalidOperation
            products = products.filter(price__lte=max_price)

        if (
            min_price not in (None, '')
            and max_price not in (None, '')
            and min_price > max_price
        ):
            return Response(
                {"error": "minprice cannot exceed maxprice"},
                status=status.HTTP_400_BAD_REQUEST
            )

    except (InvalidOperation, TypeError, ValueError):
        return Response(
            {"error": "Prices must be valid non-negative numbers"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = ProductSerializer(
        products.distinct(),
        many=True
    )

    return Response(serializer.data, status=status.HTTP_200_OK)
