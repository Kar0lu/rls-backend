from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from backend.models import (Device,
                            Container,
                            Reservation,
                            DeviceType)

from calendar import monthrange

from pprint import pprint


def device_availability(device_types, year, month, **kwargs):

    to_return = {}
    
    for device_type in device_types:
        try: devices = Device.objects.all().filter(pk__in = kwargs["dev_pk"])
        except: devices = Device.objects.all().filter(device_type__pk = device_type)
        if len(list(devices)) == 0: raise NotFound(detail = f'No devices of type {device_type} found.')
        to_return[device_type] = {}

        for device in devices:
            try: device_reservations = device.reservations.filter(valid_since__year = year, valid_since__month = month, valid_since__day = kwargs["day"])
            except: device_reservations = device.reservations.filter(valid_since__year = year, valid_since__month = month)
            
            to_return[str(device_type)][str(device.pk)] = {
                str(day).zfill(2):{str(i).zfill(2): True if i != 23 else False for i in range(0,24)}
                for day in range(1, monthrange(year, month)[1]+1)
            }

            for reservation in device_reservations:
                start_slot = reservation.valid_since.time().hour
                end_slot = reservation.valid_until.time().hour
                for slot in range(start_slot, end_slot):
                    to_return[str(device_type)][str(device.pk)][str(reservation.valid_since.day).zfill(2)][str(slot).zfill(2)] = False

    return to_return



def container_availability(year, month, **kwargs):

    try: all_containers = list(Container.objects.get(pk = kwargs["ct_pk"], available = True))
    except: all_containers = list(Container.objects.all().filter(available = True))
    to_return = {}
    for container in all_containers:
        
        to_return[str(container.pk)] = {str(day).zfill(2):{str(i).zfill(2): True if i != 23 else False for i in range(0,24)}
                                         for day in range(1, monthrange(year, month)[1]+1)}
        try: container_reservations_this_month = container.reservations_rel.filter( valid_since__year = year,
                                                                                    valid_since__month = month,
                                                                                    valid_since__day = kwargs["day"])
        except: container_reservations_this_month = container.reservations_rel.filter( valid_since__year = year,
                                                                                       valid_since__month = month)
       
        for reservation in container_reservations_this_month:
            start_slot = reservation.valid_since.time().hour
            end_slot = reservation.valid_until.time().hour
            for slot in range(start_slot, end_slot):
                to_return[str(container.pk)][str(reservation.valid_since.day).zfill(2)][str(slot).zfill(2)] = False
 

    return to_return


def compute_day(year, month, day, device_types):
    ct_reservations = container_availability(year, month, kwargs = {"day": day})
    dev_reservations = device_availability(device_types, year, month, kwargs = {"day": day})

    tday = str(day).zfill(2)
    tmonth = str(month).zfill(2)
    tyear = str(year).zfill(2)
    tdate = f'{tday}.{tmonth}.{tyear}'

    to_return = {
        tdate: []
    }

    # Karol v2
    for hour in range(0, 24):
        thour = str(hour).zfill(2)
        frontend_row = {"id": hour, "containers": {}, "devices": []}

        # Process containers
        for ct_key, ct_value in ct_reservations.items():
            container_status = ct_value[tday][thour]
            frontend_row["containers"][ct_key] = container_status

            # If container is true, check if there is at least one device of each type with true value
            if container_status:
                all_device_types_valid = True

                # Check devices for the current container
                for dev_type_key, dev_type_value in dev_reservations.items():
                    device_found = False
                    for dev_key, dev_value in dev_type_value.items():
                        if dev_value[tday][thour]:
                            device_found = True
                            break
                    if not device_found:
                        all_device_types_valid = False
                        break

                # If the container is valid, we keep it true, else set it false
                if not all_device_types_valid:
                    frontend_row["containers"][ct_key] = False

        # Process devices
        for dev_type_key, dev_type_value in dev_reservations.items():
            for dev_key, dev_value in dev_type_value.items():
                if dev_value[tday][thour]:  # Only add devices with true value
                    frontend_row["devices"].append(dev_key)  # Append device ID to the list

        to_return[tdate].append(frontend_row)

    # Karol v1
    # for hour in range(0, 24):
    #     thour = str(hour).zfill(2)
    #     backend_row = {"id": hour, "containers": {}, "devices": {}}

    #     for ct_key, ct_value in ct_reservations.items():
    #         backend_row["containers"][ct_key] = ct_value[tday][thour]

    #     for dev_type_key, dev_type_value in dev_reservations.items():
    #         backend_row["devices"][dev_type_key] = {}
    #         for dev_key, dev_value in dev_type_value.items():
    #             backend_row["devices"][dev_type_key][dev_key] = dev_value[tday][thour]
            
    #     to_return[tdate].append(backend_row)

    # Kacper
    # for ct_id, day_av in ct_reservations.items():
    #     for day_of_av, av in day_av.items():
    #         if not True in list(av.values()): continue
    #         if day_of_av == tday: to_return[tdate]["containers"].append({
    #             "ct_id": str(ct_id), "availability": list(av.values())})

    # for dev_id, day_av in dev_reservations.items():
    #     dev_type = DeviceType.objects.get(devices__pk = dev_id).pk
    #     for day_of_av, av in day_av.items():
    #         if not True in list(av.values()): continue
    #         if day_of_av == tday: to_return[tdate]["devices"].append({
    #             "dev_id": str(dev_id), "dev_type": str(dev_type), "availability": list(av.values())})

    return to_return 



def group_devices_availability(devices_availability, year, month):
    grouped_by_device_type = {}

    for device_type, devices in devices_availability.items():
        # Generating structure: {"<day>": {"HH": <boolean>, ...}, ...}
        grouped_by_device_type[device_type] = { str(day).zfill(2):
                                                {str(i).zfill(2): True
                                                for i in range(0,24) }
                                                for day in range(1, monthrange(year, month)[1]+1)}
        # temp: { "<day>": [ [ <boolean>, <boolean>, ... ], [ <boolean>, <boolean>, ... ], ...]} where booleans are ordered by hour
        temp = {}
        for availability in devices.values():
            for day in range(1, monthrange(year, month)[1]+1):
                try: temp[str(day).zfill(2)]
                except: temp[str(day).zfill(2)] = []
                temp[str(day).zfill(2)].append(list(availability[str(day).zfill(2)].values()))

        for day, grouped_availability in temp.items():
            for hour in range(0,24):
                av_this_hour = []
                for row in grouped_availability:
                    av_this_hour.append(row[hour])
                if not (True in av_this_hour):
                    grouped_by_device_type[device_type][str(day).zfill(2)][str(hour).zfill(2)] = False

    # Summing into all selected devices availability
    to_return = { str(day).zfill(2):
                 {str(i).zfill(2): True
                 for i in range(0,24) }
                 for day in range(1, monthrange(year, month)[1]+1)}

    for dt_availability in grouped_by_device_type.values():
        for day in range(1, monthrange(year, month)[1]+1):
            for hour in range(0,24):
                to_return[str(day).zfill(2)][str(hour).zfill(2)] &= dt_availability[str(day).zfill(2)][str(hour).zfill(2)]        

    return to_return

                
        
        


def compute_month(device_types, year, month):
    devices_availability = {}
    for device_type in device_types:
        devices_availability[str(device_type)] = {}

        try: all_devices_this_type = Device.objects.all().filter(device_type__pk = device_type)
        except: raise NotFound(detail = f'No devices of type {device_type} found.')

        for device_this_type in all_devices_this_type:
            reservations_this_device_this_type = Reservation.objects.all().filter(valid_since__year = year,
                                                                                  valid_since__month = month,
                                                                                  devices__pk = device_this_type.pk).values("valid_since",
                                                                                                                            "valid_until")
            # Generating structure: {"<day>": {"HH": <boolean>, ...}, ...}
            devices_availability[str(device_type)][str(device_this_type.pk)] = { str(day).zfill(2):
                                                                                {str(i).zfill(2): True
                                                                                 for i in range(0,24) }
                                                                                 for day in range(1, monthrange(year, month)[1]+1)}
            for reservation in reservations_this_device_this_type:
                start_slot = reservation["valid_since"].time().hour
                end_slot = reservation["valid_until"].time().hour
                for slot in range(start_slot, end_slot):
                    devices_availability[str(device_type)][str(device_this_type.pk)][str(reservation["valid_since"].day).zfill(2)][str(slot).zfill(2)] = False


    grouped_devices_availability = group_devices_availability(devices_availability, year, month)
    cts_availability = container_availability(year, month)

    ct_grouped = { str(day).zfill(2):
                 {str(i).zfill(2): False
                 for i in range(0,24) }
                 for day in range(1, monthrange(year, month)[1]+1)}

    for ct_availability in cts_availability.values():
        for day in range(1, monthrange(year, month)[1]+1):
            for hour in range(0,24):
                ct_grouped[str(day).zfill(2)][str(hour).zfill(2)] |= ct_availability[str(day).zfill(2)][str(hour).zfill(2)]

    grouped_all = { str(day).zfill(2):
                 {str(i).zfill(2): False
                 for i in range(0,24) }
                 for day in range(1, monthrange(year, month)[1]+1)}
    
    
    for day in range(1, monthrange(year, month)[1]+1):
            for hour in range(0,24):
                grouped_all[str(day).zfill(2)][str(hour).zfill(2)] = (ct_grouped[str(day).zfill(2)][str(hour).zfill(2)] & 
                                                        grouped_devices_availability[str(day).zfill(2)][str(hour).zfill(2)])
                 # Maintanance break
                if hour == 23: grouped_all[str(day).zfill(2)][str(hour).zfill(2)] = False

        
                
    to_return = {f'{str(month).zfill(2)}.{str(year).zfill(2)}': []}
    for day in range(1, monthrange(year, month)[1]+1):
        if not (True in list(grouped_all[str(day).zfill(2)].values())):
            to_return[f'{str(month).zfill(2)}.{str(year).zfill(2)}'].append(False)
            continue
        to_return[f'{str(month).zfill(2)}.{str(year).zfill(2)}'].append(True)

    return to_return
        


class SchedulerAvailability(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        result = {}
        device_types = request.query_params.getlist('device_types')
        year = int(request.query_params.get('year'))
        month = int(request.query_params.get('month'))
        if bool(request.query_params.get('day')):
            day = int(request.query_params.get('day'))
            result = compute_day(year, month, day, device_types)

            return Response(result, status = status.HTTP_200_OK)

        result = compute_month(device_types, year, month)      

        return Response(result, status = status.HTTP_200_OK)
