from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from tutorial.quickstart.serializers import GroupSerializer, UserSerializer
from backend.models.Container import Container
from backend.auth.authentication_classes import IsAdminOrReadOnly
from backend.models.Device import Device
from backend.models.Reservation import Reservation
from datetime import datetime
import json
from django.http import HttpResponse

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



class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime)):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


class ContainerAvailability(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            date_string = body['date']
            if 'T' in date_string:
                date_string = date_string.split('T')[0]
            date = datetime.strptime(date_string, '%Y-%m-%d').date()
            taken_dates = Reservation.objects.filter(container = pk).filter(valid_since__date = date).values("valid_since", "valid_until")
            result = []
            for td in taken_dates:
                 result.append({"valid_since": td["valid_since"], "valid_until": td["valid_until"]})
            result = str(json.dumps(result, cls = DateTimeEncoder, indent = 4))
            result = result[1:-1]
            result = '{' + result + '}'
            return HttpResponse(result)