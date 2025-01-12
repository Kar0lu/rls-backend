import uuid
from django.db import models

class Device(models.Model):
    '''Stores single Device entry.'''
    device_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 150)
    device_path = models.FilePathField(path='/tools', allow_folders = True, allow_files = False) # TODO: check if this works for directory paths