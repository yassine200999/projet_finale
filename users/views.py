from users.models import User
from rest_framework.response import Response
from users.serializers import SignUpSerializer, UpdateUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.http import require_http_methods
from rest_framework import status
from App.app import JWTAuthentication
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
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
        return Response({"error": "user not found"},status=status.HTTP_404_NOT_FOUND)
    serializer = UpdateUserSerializer(
        user,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "user update successfuly","data": serializer.data }, status=status.HTTP_200_OK
        )
    return Response({"error": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@require_http_methods(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def toogle_user(request,user_id):
    try:
        user=User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "user not found"},status=status.HTTP_404_NOT_FOUND)
    user.is_active = not user.is_active
    user.save()
    return Response(
            {"message": "user update successfuly"}, status=status.HTTP_200_OK)
@api_view(['PUT'])
@require_http_methods(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request,user_id):
    try:
        user=User.objects.get(id=user_id)
    except User.DoesNotExist:
            return Response({"error": "user not found"},status=status.HTTP_404_NOT_FOUND)
    data=request.data
    if check_password(data['current_passowrd'],user.password):
        if data['new_password']==data['comfirm_password']:
            user.password = make_password(data['new_password'])
            user.save()
            return Response({"message":"passworrd update successfuly"},status=status.HTTP_200_OK)
        else:
            return Response({"error":"password not confirm"},status=status.HTTP_404_NOT_FOUND)
    else:
            return Response({"error":"password not confirm"},status=status.HTTP_404_NOT_FOUND)