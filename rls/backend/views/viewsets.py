from rest_framework import viewsets, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import PermissionDenied, ParseError

from datetime import datetime

from backend.auth.permission_classes import (IsAdminOrReadOnly,
                                            IsOwnerOrAdmin)
from rest_framework.permissions import IsAuthenticated

from backend.models import (Device,
                            Container,
                            Reservation,
                            DeviceType,
                            Offence)

from backend.views.availability import (container_availability,
                                        device_availability)

from backend.serializers import (ContainerSerializer, 
                                DeviceSerializer,
                                ReservationSerializer,
                                DeviceTypeSerializer,
                                UserSerializer,
                                OffenceSerializer,
                                ReservationWithUserAndDevicesDataSerializer)

from django.contrib.auth import get_user_model

User = get_user_model()




class UserViewSet(mixins.RetrieveModelMixin, 
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin & IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.is_staff == True:
            return super().list(self, request, args, kwargs)
        
        raise PermissionDenied(detail = 'List function is not available for non-admin users. This situation will be reported to admin.')
    


class CreateUser(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all().order_by("pk")
    serializer_class = ContainerSerializer
    permission_classes = [IsAdminOrReadOnly & IsAuthenticated]


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by("pk")
    serializer_class = DeviceSerializer
    permission_classes = [IsAdminOrReadOnly & IsAuthenticated]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by("pk")
    serializer_class = ReservationSerializer
    permission_classes = [IsOwnerOrAdmin & IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try: 
            container = str(request.data["container"])
            devices = list(request.data["devices"])
            start_date = datetime.fromisoformat(request.data["valid_since"])
            end_date = datetime.fromisoformat(request.data["valid_until"])
        except: raise ParseError(detail = "Wrong request format")
        if (start_date.day != end_date.day) or (start_date.time().hour > end_date.time().hour):
            raise ParseError(detail = "Wrong reservation dates.")
        
        kwargs = {"ct_pk": container}
        ct_availability = container_availability(start_date.year, start_date.month, **kwargs)
        ct_availability = ct_availability[container][str(start_date.day).zfill(2)]

        for slot, av in ct_availability.items():
            if int(slot) in range(start_date.time().hour, end_date.time().hour) and av == False:
                raise ParseError(detail = "Container is unavailable in selected time.")
            
        kwargs = {'day': start_date.day, 'dev_pk': devices}
        dev_availability = device_availability([1], start_date.year, start_date.month, **kwargs)
        for device in devices:
            dev_av = dev_availability[device][str(start_date.day).zfill(2)]
            for slot, av in dev_av.items():
                if int(slot) in range(start_date.time().hour, end_date.time().hour) and av == False:
                    raise ParseError(detail = f'Device {device} is unavailable in selected time.')
                
        return super().create(request, *args, **kwargs)


    def get_serializer_class(self):
        try: extra = bool(self.request.GET.get("extra"))
        except: extra = False
        if extra == True:
            return ReservationWithUserAndDevicesDataSerializer
        return ReservationSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_staff == True:
            return super().list(self, request, args, kwargs)
        
        raise PermissionDenied(detail = 'List function is not available for non-admin users. This situation will be reported to admin.')


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all().order_by("pk")
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAdminOrReadOnly & IsAuthenticated]


class OffenceViewSet(viewsets.ModelViewSet):
    queryset = Offence.objects.all().order_by("-commited_at")
    serializer_class = OffenceSerializer
    permission_classes = [IsAdminOrReadOnly & IsAuthenticated]