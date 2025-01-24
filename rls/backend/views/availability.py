from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from backend.models.Device import Device
from backend.models.Container import Container

from calendar import monthrange

from json import loads

def device_availability(device_types, year, month):

    to_return = {}
    
    for device_type in device_types:

        try:
            devices = Device.objects.all().filter(device_type__pk = device_type)
        except:
            raise NotFound(detail = f'No devices of type {device_type} found.')

        for device in devices:
            device_reservations = device.reservations.filter(valid_since__year = year, valid_since__month = month)
            to_return[str(device.pk)] = {str(day).zfill(2):{str(i).zfill(2): True for i in range(0,24)} for day in range(1, monthrange(year, month)[1]+1)}

            for reservation in device_reservations:
                start_slot = reservation.valid_since.time().hour
                end_slot = reservation.valid_until.time().hour
                for slot in range(start_slot, end_slot):
                    to_return[str(device.pk)][str(reservation.valid_since.day).zfill(2)][str(slot).zfill(2)] = False

    return to_return



def container_availability(year, month):

    all_containers = list(Container.objects.all().filter(available = True))
    to_return = {}
    for container in all_containers:
        
        to_return[str(container.pk)] = {str(day).zfill(2):{str(i).zfill(2): True for i in range(0,24)} for day in range(1, monthrange(year, month)[1]+1)}
        container_reservations_this_month = container.reservations_rel.filter(valid_since__year = year, valid_since__month = month)
       
        for reservation in container_reservations_this_month:
            start_slot = reservation.valid_since.time().hour
            end_slot = reservation.valid_until.time().hour
            for slot in range(start_slot, end_slot):
                to_return[str(container.pk)][str(reservation.valid_since.day).zfill(2)][str(slot).zfill(2)] = False

    return to_return




class SchedulerAvailability(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        result = {}
        year = int(request.query_params.get('year'))
        month = int(request.query_params.get('month'))
        device_types = request.query_params.getlist('device_types')
        
        devices_reservations = device_availability(device_types, year, month)
        ct_availability = container_availability(year, month)

        for day in range(1, monthrange(year, month)[1]+1):
            day = str(day).zfill(2)
            result[day] = {}
            result[day]["devices"] = {}
            for device_id in devices_reservations.keys():
                result[day]["devices"][str(device_id)] = devices_reservations[device_id][day]
            result[day]["containers"] = {}
            for ctid in ct_availability.keys():
                result[day]["containers"][ctid] = ct_availability[ctid][day]
        

        return Response(result, status = status.HTTP_200_OK)
