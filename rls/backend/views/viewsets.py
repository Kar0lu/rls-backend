from rest_framework import viewsets, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import PermissionDenied

from backend.auth.permission_classes import (IsAdminOrReadOnly,
                                            IsOwnerOrAdmin)
from rest_framework.permissions import IsAuthenticated

from backend.models import (Device,
                            Container,
                            Reservation,
                            DeviceType,
                            Offence)

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