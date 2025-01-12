import uuid
from django.db import models
from .Device import Device
from .Reservation import Reservation

class Device_Reservation(models.Model):
    '''Bridging table to store information about reservation of particular device'''
    device_reservation_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    device = models.ForeignKey(Device, on_delete = models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete = models.CASCADE)