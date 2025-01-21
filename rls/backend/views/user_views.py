from copy import deepcopy
from rest_framework import permissions

from django.http import JsonResponse
from rest_framework.views import APIView

from backend.models.Reservation import Reservation
from backend.models.Device import Device
from backend.models.Container import Container

from datetime import datetime
from calendar import monthrange

from json import loads

def flip_taken(device_reservations, date, default_not_taken):
    to_return = deepcopy(default_not_taken)
    for device_id, reservations in device_reservations.items():
        if not len(reservations) == 0:
            for reservation in reservations:
                if reservation.valid_since.day == date.day:
                    start_slot = reservation.valid_since.time().hour
                    number_of_slots = reservation.valid_until.time().hour - reservation.valid_since.time().hour
                    for slot in range(start_slot, number_of_slots):
                        reserved_devices_ids = []
                        for reserved_device in list(reservation.devices.all()):
                            reserved_devices_ids.append(reserved_device.pk)
                        for device_id in reserved_devices_ids:
                            to_return[str(device_id)][str(slot).zfill(2)] = False
    return to_return

def container_availability(year, month, time_slots):
    all_containers = list(Container.objects.all().filter(available = True))
    to_return = {}
    for container in all_containers:
        
        to_return[str(container.pk)] = {str(day).zfill(2):deepcopy(time_slots) for day in range(1, monthrange(year, int(month))[1]+1)}
        container_reservations_this_month = container.reservations_rel.filter(valid_since__year = year, valid_since__month = month)
        if len(list(container_reservations_this_month)) == 0:
            continue
       
        for reservation in container_reservations_this_month:
            start_slot = reservation.valid_since.time().hour
            end_slot = reservation.valid_until.time().hour
            for slot in range(start_slot, end_slot):
                to_return[str(container.pk)][str(reservation.valid_since.day).zfill(2)][str(slot).zfill(2)] = False


    return to_return




class SchedulerAvailability(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        result = {}
        body = loads(request.body.decode('utf-8'))
        year = int(body['year'])
        month = int(body['month'])
        device_types = body['device_types']
        time_slots = {str(i).zfill(2): True for i in range(0,24)}
        day = {}
        devices = {}
        devices_reservations = {}
        for device_type in device_types:
            temp_devices = Device.objects.all().filter(device_type__pk = device_type).values("pk") # Find all devices of such type and store its id
            for temp_device in temp_devices:
                devices_reservations[str(temp_device['pk'])] = Reservation.objects.all().filter(valid_since__year = year,
                                                                                                valid_since__month = month,
                                                                                                devices__pk = temp_device['pk'])
                devices[str(temp_device['pk'])] = deepcopy(time_slots) # each device id appended as a key to available time slots

        month = str(month).zfill(2)
        ct_availability = container_availability(year, month, time_slots)

        for day in range(1, monthrange(year, int(month))[1]+1):
            day = str(day).zfill(2)
            result[day] = {}
            result[day]["devices"] = flip_taken(devices_reservations, datetime.strptime(str(year) + month + day, "%Y%m%d"), devices)
            result[day]["containers"] = {}
            for ctid in ct_availability.keys():
                result[day]["containers"][ctid] = ct_availability[ctid][day]
        

        return JsonResponse(result)
