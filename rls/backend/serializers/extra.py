from rest_framework import serializers

from backend.models import (DeviceType,
                            Reservation,
                            Device)
from backend.serializers import ContainerSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

class UserFirstAndLastNames(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']
        extra_kwargs = {'id': { 'read_only': True},
                        'first_name': { 'read_only': True},
                        'last_name': { 'read_only': True}}
        

class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ["device_type_id", "make", "model", "description"]
        extra_kwargs = { 'device_type_id': { 'read_only': True },
                         'make': { 'read_only': True },
                         'model': { 'read_only': True },}


class DeviceSerializer(serializers.ModelSerializer):

    device_type = DeviceTypeSerializer(Device.objects.all())

    class Meta:
        model = Device
        fields = ["device_id", "device_type"]
        extra_kwargs = { 'device_type': { 'required': False },
                        'device_id': { 'read_only': True } }
        

class ReservationWithUserAndDevicesDataSerializer(serializers.ModelSerializer):

    devices = DeviceSerializer(read_only = True, many = True)
    user = UserFirstAndLastNames(read_only = True)
    container = ContainerSerializer(read_only = True)

    class Meta:
        model = Reservation
        fields = ["reservation_id", "created_at", "valid_since", "valid_until", "devices", "container", "user", "root_password", "status"]
        extra_kwargs = { 'reservation_id': { 'read_only': True },
                         'created_at': { 'read_only': True },
                         'valid_since': { 'read_only': True },
                         'valid_until': { 'read_only': True },
                         'devices': { 'read_only': True },
                         'container': { 'read_only': True },
                         'user': { 'read_only': True },
                         'root_password': { 'read_only': True },
                         'status': { 'read_only': True }, }