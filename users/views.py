from users.models import User
from rest_framework.response import Response
from users.serializers import SignUpSerializer, UpdateUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.http import require_http_methods
from rest_framework import status
from App.app import JWTAuthentication


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


@api_view(['POST'])
@require_http_methods(['POST'])
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
                "message": "user update successfuly",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {"error": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )