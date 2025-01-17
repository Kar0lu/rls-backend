from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from tutorial.quickstart.serializers import GroupSerializer, UserSerializer
from backend.auth.authentication_classes import IsAdminOrReadOnly

from backend.models.Device import Device
from backend.models.Container import Container
from backend.models.Reservation import Reservation
from backend.models.DeviceType import DeviceType

from backend.serializers import ContainerSerializer, DeviceSerializer, ReservationSerializer, DeviceTypeSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all().order_by("pk")
    serializer_class = ContainerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by("pk")
    serializer_class = DeviceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by("pk")
    serializer_class = ReservationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]            # Temporary, change to custom permissions


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all().order_by("pk")
    serializer_class = DeviceTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]