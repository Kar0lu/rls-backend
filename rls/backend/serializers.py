from rest_framework import serializers

from backend.models.Container import Container
from backend.models.Device import Device
from backend.models.Dictionary import Dictionary
from backend.models.Reservation import Reservation
from backend.models.DeviceType import DeviceType
from backend.models.Offence import Offence
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    reservations = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'reservations']
        extra_kwargs = {'id': {'read_only': True}}


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ["container_id", "ip_address","port", "available", "name"]
        extra_kwargs = {'container_id': {'read_only': True}}


class DeviceSerializer(serializers.ModelSerializer):

    reservations = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

    class Meta:
        model = Device
        fields = ["device_id", "device_type", "device_path", "reservations"]
        extra_kwargs = {'reservations': {'required': False},
                        'device_id': {'read_only': True}}

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
        extra_kwargs = {'devices': {'required': False},
                        'reservation_id': {'read_only': True}}


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ["device_type_id", "make", "model", "description"]
        extra_kwargs = {'device_type_id': {'read_only': True}}


class OffenceSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), required = True)

    class Meta:
        model = Offence
        fields = ["offence_id", "commited_at", "description", "user"]
        extra_kwargs = {'offence_id': {'read_only': True}}
