import uuid
from django.db import models
from django.contrib.auth.models import User


class Container(models.Model):
    container_id = models.SmallAutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    available = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    init_script = models.FilePathField(path = '/root/deploy_scripts')
    # TODO: ask if users will be able to (specify ct resources)/(view ct resources will be visible to users)


class Device(models.Model):
    device_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 150)
    device_path = models.FilePathField(path='/tools', allow_folders = True, allow_files = False) # TODO: check if this works for directory paths


class Reservation(models.Model):
    reservation_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_since = models.DateTimeField()
    valid_until = models.DateTimeField()
    container = models.ForeignKey(Container, on_delete = models.CASCADE)
    devices = models.ManyToManyField(Device, through = "Device_Reservation")
    user = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    root_password = models.CharField(max_length = 20)


class Device_Reservation(models.Model):
    device_reservation_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    device = models.ForeignKey(Device, on_delete = models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete = models.CASCADE)


class Dictionary(models.Model):
    dictionary_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    sudo_name = models.CharField(max_length = 6)
    sudo_password = models.CharField(max_length = 15)
    

