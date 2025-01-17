from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

from django.http import HttpResponse
from rest_framework.views import APIView

from backend.models.Reservation import Reservation

from datetime import datetime

from json import loads

class ContainerAvailability(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = loads(body_unicode)
            date_string = body['date']
            if 'T' in date_string:
                date_string = date_string.split('T')[0]
            date = datetime.strptime(date_string, '%Y-%m-%d').date()
            taken_dates = Reservation.objects.filter(container = pk).filter(valid_since__date = date).values("valid_since", "valid_until")
            result = []
            for td in taken_dates:
                 result.append({"valid_since": td["valid_since"], "valid_until": td["valid_until"]})

            result = {"data": result}
            return HttpResponse(result)