from django.db import models

class Container(models.Model):
    '''Stores single Container entry.'''
    container_id = models.SmallAutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    port = models.SmallIntegerField()
    available = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    init_script = models.FilePathField(path = '/root/deploy_scripts')