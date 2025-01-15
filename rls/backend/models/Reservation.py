import uuid
from django.db import models
from .Container import Container
from .Device import Device
from django.contrib.auth.models import User

class Reservation(models.Model):
    '''Stores single Reservation. Related to one :model:`backend.Container`, many :model:`backend.Device` and one :model:`auth.User`.'''
    reservation_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_since = models.DateTimeField()
    valid_until = models.DateTimeField()
    container = models.ForeignKey(Container, on_delete = models.CASCADE)
    devices = models.ManyToManyField(Device, through = "Device_Reservation")
    user = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    root_password = models.CharField(max_length = 20)

    USES = (
        ("PD", "Pending"),
        ("IP", "In progress"),
        ("FI", "Finished"),
    )
    status = models.CharField(
        max_length = 2,
        choices = USES,
        default = "PD",
    )