from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework.response import Response
from backend.serializers import ReservationWithUserAndDevicesDataSerializer
from backend.models import Reservation

from django.contrib.auth import get_user_model
User = get_user_model()

class ListUserReservations(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = Reservation.objects.all().filter(user__pk = request.user.pk)
        serializer = ReservationWithUserAndDevicesDataSerializer(reservations, many=True)
        return Response(serializer.data)