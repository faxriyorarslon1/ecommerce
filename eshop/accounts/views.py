from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.http import QueryDict
import numpy as np
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from accounts.utils import generate_access_token, generate_refresh_token
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

user_response = openapi.Response('response description', SendCodeSerializer)
@swagger_auto_schema(methods=['post'],request_body=SendCodeSerializer)
@api_view(['POST',])
def send_code(request):
     if request.method == 'POST':
          serializer = SendCodeSerializer(data = request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)


user_response = openapi.Response('response description', RegisterCustomerSerializer)
@swagger_auto_schema(methods=['post'],request_body=RegisterCustomerSerializer)
@api_view(['POST',])
def register_customer(request):
     if request.method == 'POST':
          serializer = RegisterCustomerSerializer(data = request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          print(serializer.data)
          return Response(data=serializer.data, status=status.HTTP_201_CREATED)



user_response = openapi.Response('response description', CustomerLoginSerializer)
@swagger_auto_schema(methods=['post'],request_body=CustomerLoginSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def customer_login_view(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    response = Response()
    if (phone is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'phone number and password required')
    user = CustomUser.objects.filter(phone=phone).last()
    print(make_password(password))
    if(user is None):
          raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')
    serialized_user = CustomerLoginSerializer(user).data
    serialized_user.pop('password')
    refresh_token = RefreshToken().for_user(user)
    access_token = str(RefreshToken().for_user(user).access_token)
    refresh_token = str(refresh_token.access_token)
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'refresh_token': refresh_token, 
        'user': serialized_user,
    }
    return response



user_response = openapi.Response('response description', SendSMSToChangePassswordSerializer)
@swagger_auto_schema(methods=['post'],request_body=SendSMSToChangePassswordSerializer)
@api_view(['POST',])
def send_code_change_password_or_phone(request):
    serializer = SendSMSToChangePassswordSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message":"Send message to phone number"}, status=status.HTTP_200_OK)


user_response = openapi.Response('User Password change', ChangePassswordSerializer)
@swagger_auto_schema(methods=['post'],request_body=ChangePassswordSerializer)
@api_view(['POST',])
def change_password(request):
    serializer = ChangePassswordSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message":"User Password changed"}, status=status.HTTP_200_OK)


user_password_response = openapi.Response('User Phone Change', ChangePhoneSerializer)
@swagger_auto_schema(methods=['post'],request_body=ChangePhoneSerializer)
@api_view(['POST',])
def change_phone(request):
    serializer = ChangePhoneSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message":"User phone number changed"}, status=status.HTTP_200_OK)


class CustomerProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomerProfileSerializer

    def patch(self, request, *args, **kwargs):
        pic = request.FILES["pic"]
        request.data.update({"user": {"pic":pic}})
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        return Customer.objects.get(user=self.request.user)



