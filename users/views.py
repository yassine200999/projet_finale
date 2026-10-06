from users.models import User
from rest_framework.response import Response
from users.serializers import SignUpSerializer, UpdateUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.http import require_http_methods
from rest_framework import status
from App.app import JWTAuthentication
from django.contrib.auth.hashers import check_password, make_password


@api_view(['POST'])
@require_http_methods(['POST'])
@permission_classes([AllowAny])
def add_user(request):
    serializer = SignUpSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'account created'},
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT'])
@require_http_methods(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(
            {"error": "user not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = UpdateUserSerializer(
        user,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "user update successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {"error": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT'])
@require_http_methods(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def toogle_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "user not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    user.is_active = not user.is_active
    user.save()

    return Response(
        {"message": "user updated successfully"},
        status=status.HTTP_200_OK
    )


@api_view(['PUT'])
@require_http_methods(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "user not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not current_password or not new_password or not confirm_password:
        return Response(
            {
                "error": "current_password, new_password and confirm_password are required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if not check_password(current_password, user.password):
        return Response(
            {"error": "Current password is incorrect"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_password != confirm_password:
        return Response(
            {"error": "New passwords do not match"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.password = make_password(new_password)
    user.save(update_fields=['password'])

    return Response(
        {"message": "Password updated successfully"},
        status=status.HTTP_200_OK
    )
