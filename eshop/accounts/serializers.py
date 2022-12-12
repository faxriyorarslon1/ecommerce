from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import *
import requests
from django.contrib.auth.hashers import make_password


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    kod = serializers.IntegerField()

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        kod = validated_data.pop('kod')
        ex = CustomUser.objects.filter(phone=phone)
        if len(ex) == 0:
            url = "http://notify.eskiz.uz/api/auth/login"
            payload={'email': 'test@eskiz.uz',
            'password': 'j6DWtQjjpLDNjWEk74Sx'}
            response = requests.request("POST", url,data=payload)
            token = response.text.split('"')[9]
            url = "http://notify.eskiz.uz/api/message/sms/send"
            payload={'mobile_phone': f'{phone}',
            'message': f'Sizning tasdiqlash kodingiz {kod}',
            'from': '4546',
            'callback_url': 'http://0000.uz/test.php'}
            headers = {
                        'Authorization': f'Bearer {token}'
                        }
            response = requests.request("POST", url, headers=headers, data=payload)

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
    # city = serializers.CharField()
    middlename = serializers.CharField(write_only=True,required=True,)
    password = serializers.CharField(
        write_only=True,required=True,
    )
    kod = serializers.IntegerField(write_only=True,required=True)
    # def get_city_obj(self, cityname):
    #     try:
    #         city = City.objects.get(name=cityname)
    #     except City.DoesNotExist:
    #         city = None
    #     return city


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
            print(phone, uu)
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
                return user
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


