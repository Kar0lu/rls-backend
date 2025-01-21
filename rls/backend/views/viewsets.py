from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from backend.auth.permission_classes import (IsAdminOrReadOnly,
                                            IsOwnerOrAdmin)
from rest_framework.permissions import IsAuthenticated

from backend.models.Device import Device
from backend.models.Container import Container
from backend.models.Reservation import Reservation
from backend.models.DeviceType import DeviceType
from backend.models.Offence import Offence

from backend.serializers import (ContainerSerializer, 
                                DeviceSerializer,
                                ReservationSerializer,
                                DeviceTypeSerializer,
                                UserSerializer,
                                OffenceSerializer)

from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
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