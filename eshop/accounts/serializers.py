from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import *
import requests
from django.contrib.auth.hashers import make_password
import numpy as np


def send_message_to_number(phone, message):
    if phone[0]=="+":
        phone = phone[1:]
    url = "http://notify.eskiz.uz/api/auth/login"
    payload={'email': 'faxriyorarslon1@gmail.com',
            'password': 'UruW0YV9SCg1au3XDFtSf6xgRoPTBbz8qZ5wRsz1'}
    response = requests.request("POST", url,data=payload)
    token = response.text.split('"')[9]
    url = "http://notify.eskiz.uz/api/message/sms/send"
    payload={'mobile_phone': f'{phone}',
    'message': message,
    'from': '4546',
    'callback_url': 'http://0000.uz/test.php'}
    headers = {
                        'Authorization': f'Bearer {token}'
                        }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


class SendSMSToChangePassswordSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        kod = np.random.randint(10000, 99999)
        ex = CustomUser.objects.filter(phone=phone)
        if len(ex) != 0:
            message = f'Sizning parolingizni almashtirish uchun tasdiqlash kodingiz {kod}'
            send_message_to_number(phone, message)
            user = CustomUser.objects.filter(phone = phone).first()
            user.kod=kod
            user.save()
            return user
        else:
            error = {'message':'Your phone number not found'}
            raise serializers.ValidationError(error)



class ChangePassswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    new_password = serializers.CharField(required=True)
    kod = serializers.IntegerField(required=True)

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        kod = validated_data.pop('kod')
        user = CustomUser.objects.filter(phone=phone).first()
        if user is not None:
            if user.kod == kod:
                user.set_password(validated_data.get("new_password"))
                user.save()
                return user
            else:
                error = {'error':'Code is incorrect'}
                raise serializers.ValidationError(error)            
        else:
            error = {'error':'User not found'}
            raise serializers.ValidationError(error)


class ChangePhoneSerializer(serializers.Serializer):
    oldphone = serializers.CharField()
    newphone = serializers.CharField(required=True)
    kod = serializers.IntegerField(required=True)

    def create(self, validated_data):
        phone = validated_data.pop('oldphone')
        kod = validated_data.pop('kod')
        newphone = validated_data.pop('newphone')
        user = CustomUser.objects.filter(phone=phone).first()
        if user is not None:
            if user.kod == kod:
                user.phone = newphone
                user.save()
                return user
            else:
                error = {'error':'Code is incorrect'}
                raise serializers.ValidationError(error)            
        else:
            error = {'error':'User not found'}
            raise serializers.ValidationError(error)

class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def to_representation(self, instance):
        data = super(SendCodeSerializer, self).to_representation(instance)
        if not data.get('kod'):
            data.pop('kod', None)
        return data

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        kod = np.random.randint(10000, 99999)
        ex = CustomUser.objects.filter(phone=phone)
        if len(ex) == 0:
            message = f'Sizning tasdiqlash kodingiz {kod}'
            send_message_to_number(phone, message)
            obj, created = UnverifiedUsers.objects.update_or_create(
                phone=phone,
                defaults={'kod': kod},
            )
            return obj
        else:
            error = {'message':'This phone number is already registered'}
            raise serializers.ValidationError(error)


class RegisterCustomerSerializer(serializers.Serializer):
    phone = serializers.CharField(write_only=True,required=True,)
    pic = serializers.ImageField(write_only=True,required=True,)
    first_name = serializers.CharField(write_only=True,required=True,)
    last_name = serializers.CharField(write_only=True,required=True,)
    middlename = serializers.CharField(write_only=True,required=True,)
    password = serializers.CharField(
        write_only=True,required=True,
    )
    kod = serializers.IntegerField(write_only=True,required=True)


    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        password = validated_data.get('password')
        status = "Active"
        middlename = validated_data.get('middlename')
        phone = validated_data.get('phone')
        kod = validated_data.get("kod")
        try:
            uu = UnverifiedUsers.objects.filter(phone=phone).first()
        except UnverifiedUsers.DoesNotExist:
            uu = None
        if uu is None:
            error = {'message':'This phone number is not registered'}
            raise serializers.ValidationError(error)
        if kod == uu.kod:
            user = CustomUser.objects.filter(phone = phone).first()
            if user is None:
                user= CustomUser.objects.create_user(first_name=first_name, last_name=last_name, middlename=middlename,
                                                phone = phone, username=first_name+phone, status = status, kod=kod, role="Customer", password=password)
                customer = Customer.objects.create(user=user)
                sdata = {
                    "first_name":first_name,
                    "last_name":last_name
                }
                return sdata
            else:
                error = {'message':'User already registered'}
                raise serializers.ValidationError(error)

        else:
            error = {'message':'Your phone number not found'}
            raise serializers.ValidationError(error)


class CustomerLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("phone", "password", "first_name", "last_name", "status")
        read_only_fields = ("first_name", "last_name", "status")



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "pic")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("name",)

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True, many=False)

    class Meta:
        model = Customer
        fields = ('user', 'city', 'discard', 'ginfo')


    def update(self, instance, validated_data):
        if instance.user.phone:
            user = CustomUser.objects.get(phone=instance.user.phone)
            if "user" in validated_data.keys():
                user_data = validated_data.get('user')
                user_serializer = UserSerializer(data=user_data)
                user_serializer.is_valid(raise_exception=True)
                user_serializer.update(user, user_data)
            instance.save()
            return instance







