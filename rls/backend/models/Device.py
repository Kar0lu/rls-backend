import uuid
from django.db import models

from .DeviceType import DeviceType

class Device(models.Model):
    '''Stores single Device entry.'''
    device_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    device_type = models.ForeignKey(DeviceType, on_delete = models.CASCADE)
    device_path = models.CharField(null = False, blank = False, max_length = 100)