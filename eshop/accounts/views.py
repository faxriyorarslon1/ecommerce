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

user_response = openapi.Response('response description', SendCodeSerializer)
@swagger_auto_schema(methods=['post'],request_body=SendCodeSerializer)
@api_view(['POST',])
def send_code(request):
     if request.method == 'POST':
          if isinstance(request.data, QueryDict): # optional
               request.data._mutable = True
          code = np.random.randint(10000, 99999)
          request.data['kod'] = code
          serializer = SendCodeSerializer(data = request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
          # return Response({"message":"Phone number field is empty!"
          #                     },status=status.HTTP_400_BAD_REQUEST)


user_response = openapi.Response('response description', RegisterCustomerSerializer)
@swagger_auto_schema(methods=['post'],request_body=RegisterCustomerSerializer)
@api_view(['POST',])
def register_customer(request):
     if request.method == 'POST':
          serializer = RegisterCustomerSerializer(data = request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)



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
    if(user is None):
          raise exceptions.AuthenticationFailed('user not found')
    print(user.username, password)
    user = authenticate(request, username=user.username, password=password)
    serialized_user = CustomerLoginSerializer(user).data
    serialized_user.pop('password')
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'refresh_token': refresh_token, 
        'user': serialized_user,
    }
    return response
