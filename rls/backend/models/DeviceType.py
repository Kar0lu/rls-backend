import uuid
from django.db import models

class DeviceType(models.Model):
    '''Stores information about Device type'''
    device_type_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    make = models.CharField(max_length = 150, null = False, blank = False)
    model = models.CharField(max_length = 150, null = False, blank = False)
    description = models.CharField(max_length = 150)
