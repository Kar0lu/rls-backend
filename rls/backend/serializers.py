import os
from rest_framework import serializers

from backend.models.Container import Container
from backend.models.Device import Device
from backend.models.Dictionary import Dictionary
from backend.models.Reservation import Reservation
from backend.models.DeviceType import DeviceType
from backend.models.Offence import Offence

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    reservations = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff', 'email', 'date_joined', 'reservations', 'password']
        extra_kwargs = {'id': { 'read_only': True, 'required': False },
                        'is_staff': { 'read_only': True },
                        'date_joined': { 'read_only': True, 'required': False },
                        'reservations': { 'required': False }}
        
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        user_dir = f'{os.environ("DJANGO_MEDIA_ROOT")}/{str(user.pk)}'
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        return user


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ["container_id", "ip_address","port", "available", "name"]
        extra_kwargs = { 'container_id': { 'read_only': True } }


class DeviceSerializer(serializers.ModelSerializer):

    reservations = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

    class Meta:
        model = Device
        fields = ["device_id", "device_type", "device_path", "reservations"]
        extra_kwargs = { 'reservations': { 'required': False },
                        'device_id': { 'read_only': True } }

class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Dictionary
        fields = ["dictionary_id", "sudo_name", "sudo_password"]
        


class ReservationSerializer(serializers.ModelSerializer):

    devices = serializers.PrimaryKeyRelatedField(many = True, read_only = False, queryset = Device.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), required = True)

    class Meta:
        model = Reservation
        fields = ["reservation_id", "created_at", "valid_since", "valid_until", "devices", "container", "user", "root_password", "status"]
        extra_kwargs = { 'devices': { 'required': False },
                        'reservation_id': { 'read_only': True } }


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ["device_type_id", "make", "model", "description"]
        extra_kwargs = { 'device_type_id': { 'read_only': True } }


class OffenceSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), required = True)

    class Meta:
        model = Offence
        fields = ["offence_id", "commited_at", "description", "user"]
        extra_kwargs = { 'offence_id': { 'read_only': True } }
