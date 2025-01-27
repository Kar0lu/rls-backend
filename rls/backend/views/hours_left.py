from backend.auth.permission_classes import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from datetime import datetime
from os import environ

from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from django.contrib.auth import get_user_model
User = get_user_model()


def total_user_hours_left(user):
    user_reservations = user.reservations.filter(valid_since__gte = datetime.now())
    current_hours = 0

    for reservation in user_reservations:
        start = reservation.valid_since.time().hour
        end = reservation.valid_until.time().hour

        for hour in range(start, end):
            current_hours += 1
    return int(environ['MAXIMUM_RESERVATION']) - current_hours


class HoursLeft(APIView):

    permission_classes = [IsOwnerOrAdmin & IsAuthenticated]

    def get(self, request, **kwargs):

        try: kwargs["user_id"]
        except KeyError: kwargs["user_id"] = None

        if bool(kwargs["user_id"]):
            try:
                user = User.objects.get(pk = kwargs["user_id"])
                self.check_object_permissions(request, user)
            except User.DoesNotExist:
                raise NotFound(detail = f'Could not find user {kwargs["user_id"]}')
        else:
            user = request.user

        return Response({"hours_left": total_user_hours_left(user)}, status = status.HTTP_200_OK)

        

        
