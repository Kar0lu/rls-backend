from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from tutorial.quickstart.serializers import GroupSerializer, UserSerializer
from backend.models.Container import Container
from backend.auth.authentication_classes import IsAdminOrReadOnly
from backend.models.Device import Device

from backend.serializers import ContainerSerializer, DeviceSerializer


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