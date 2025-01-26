import os
from rest_framework import serializers

from backend.models import (UserProfile,
                            Offence,
                            DeviceType,
                            Reservation,
                            Device,
                            Container)

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
    hours_left = serializers.SlugRelatedField(read_only = True, source = 'profile', slug_field = 'hours_left')
    uuid = serializers.SlugRelatedField(read_only = True, source = 'profile', slug_field = 'uuid')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff', 'email', 'date_joined', 'reservations', 'password', 'hours_left', 'uuid']
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

        user_profile = UserProfile.objects.create(user = user)

        user_dir = f'{os.getenv("DJANGO_MEDIA_ROOT")}/{str(user_profile.uuid)}'
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
            os.chmod(user_dir, 0o777)

        return user
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ["container_id", "ip_address","port", "available", "name"]
        extra_kwargs = { 'container_id': { 'read_only': True } }


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ["device_type_id", "make", "model", "description"]
        extra_kwargs = { 'device_type_id': { 'read_only': True } }


class DeviceSerializer(serializers.ModelSerializer):

    reservations = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    device_type = serializers.PrimaryKeyRelatedField(queryset = DeviceType.objects.all(), many = False)

    class Meta:
        model = Device
        fields = ["device_id", "device_type", "device_path", "reservations"]
        extra_kwargs = { 'reservations': { 'required': False },
                        'device_id': { 'read_only': True } }
        


class ReservationSerializer(serializers.ModelSerializer):

    devices = serializers.PrimaryKeyRelatedField(many = True, queryset = Device.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), required = True)

    class Meta:
        model = Reservation
        fields = ["reservation_id", "created_at", "valid_since", "valid_until", "devices", "container", "user", "root_password", "status"]
        extra_kwargs = { 'devices': { 'required': False },
                        'reservation_id': { 'read_only': True } }
        
        

class OffenceSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), required = True)

    class Meta:
        model = Offence
        fields = ["offence_id", "commited_at", "description", "user"]
        extra_kwargs = { 'offence_id': { 'read_only': True } }
