from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from backend.auth.permission_classes import IsAdminOrReadOnly, IsOwnerOrAdmin

from backend.models.Device import Device
from backend.models.Container import Container
from backend.models.Reservation import Reservation
from backend.models.DeviceType import DeviceType

from backend.serializers import ContainerSerializer, DeviceSerializer, ReservationSerializer, DeviceTypeSerializer, UserSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]

    def list(self, request, *args, **kwargs):
        if request.user.is_staff == True:
            return super().list(self, request, args, kwargs)
        
        response = {'message': 'List function is not available for non-admin users.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all().order_by("pk")
    serializer_class = ContainerSerializer
    permission_classes = [IsAdminOrReadOnly]


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by("pk")
    serializer_class = DeviceSerializer
    permission_classes = [IsAdminOrReadOnly]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by("pk")
    serializer_class = ReservationSerializer
    permission_classes = [IsOwnerOrAdmin]

    def list(self, request, *args, **kwargs):
        if request.user.is_staff == True:
            return super().list(self, request, args, kwargs)
        
        response = {'message': 'List function is not available for non-admin users.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all().order_by("pk")
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAdminOrReadOnly]