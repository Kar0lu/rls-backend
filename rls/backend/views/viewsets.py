from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from backend.auth.permission_classes import IsAdminOrReadOnly, IsOwnerOrAdmin

from backend.models.Device import Device
from backend.models.Container import Container
from backend.models.Reservation import Reservation
from backend.models.DeviceType import DeviceType

from backend.serializers import ContainerSerializer, DeviceSerializer, ReservationSerializer, DeviceTypeSerializer, GroupSerializer, UserSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrAdmin]

    def list(self, request, *args, **kwargs):
        print(request)
        if request.user.is_staff == False:
            response = {'message': 'List function is not available for non-admin users.'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    permission_classes = [IsOwnerOrAdmin]

    def list(self, request, *args, **kwargs):
        if request.user.is_staff == False:
            response = {'message': 'List function is not available for non-admin users.'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all().order_by("pk")
    serializer_class = DeviceTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]