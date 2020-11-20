import jwt
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics, status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.http import Http404
from CustomUser import settings
from users.serializers import LoginSerializer, UserSerializer, RegisterSerializer, ChangePasswordSerializer
from users.utils import generate_access_token
from users.models import User


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def refresh_token_view(request):
    User = get_user_model()
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            '\'refreshtoken\' were not provided in cookie header.')
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')
    except:
        return Response(
            {"detail": "bad refresh token."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})


# class UserView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer
#
#     def get(self, request, pk, format=None):
#         print(self.request.user)
#         user = request.user
#         serializer = self.serializer_class(user)
#         return Response(serializer.data)


# class UserView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         print(user)
#         return User.objects.filter(username=user)
#
#     def patch(self, request, pk):
#         user = request.user
#         serializer = UserSerializer(user, data=request.data,
#                                          partial=True)  # set partial=True to update a data partially
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(code=201, data=serializer.data)
#         return JsonResponse(code=400, data="wrong parameters")


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                # 'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    try:
        user = request.user
        print(user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        print(user.id)
        # if not user:
        #     return Response({'detail': 'unknownS error'})
        serialized_user = UserSerializer(user).data
        return Response({'user': serialized_user})
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
