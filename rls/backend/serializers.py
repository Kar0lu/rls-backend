from django.contrib.auth.models import Group, User
from rest_framework import serializers
from backend.models.Container import Container
from backend.models.Device import Device
from backend.models.Dictionary import Dictionary
from backend.models.Reservation import Reservation

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ["container_id", "ip_address","port", "available", "name"]


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["device_id", "name", "device_path"]


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Dictionary
        fields = ["dictionary_id", "sudo_name", "sudo_password"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["reservation_id", "created_at", "valid_since", "valid_until", "container", "devices", "user", "root_password", "status"]