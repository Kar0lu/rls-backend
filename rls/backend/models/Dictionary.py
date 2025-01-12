import uuid
from django.db import models

class Dictionary(models.Model):
    '''Stores information about login credentials to container.'''
    dictionary_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    sudo_name = models.CharField(max_length = 6)
    sudo_password = models.CharField(max_length = 15)