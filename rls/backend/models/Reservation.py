import uuid
from django.db import models
from .Container import Container
from .Device import Device
from django.contrib.auth import get_user_model

User = get_user_model()

class Reservation(models.Model):
    '''Stores single Reservation. Related to one :model:`backend.Container`, many :model:`backend.Device` and one :model:`auth.User`.'''
    reservation_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_since = models.DateTimeField()
    valid_until = models.DateTimeField()
    container = models.ForeignKey(Container, on_delete = models.CASCADE, related_name = "reservations_rel")
    devices = models.ManyToManyField(Device, through = "Device_Reservation", related_name = "reservations")
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "reservations")
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
