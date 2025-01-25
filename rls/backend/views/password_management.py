from backend.serializers import ChangePasswordSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

User = get_user_model()

class ChangePassword(GenericAPIView):

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, id):
        new_password = request.data['new_password']
        obj = get_user_model().objects.get(pk=id)
        obj.set_password(new_password)
        obj.save()
        return Response({'success': 'password changed successfully'}, status=200)