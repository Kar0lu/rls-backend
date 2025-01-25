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
        password = request.data['password']
        new_password = request.data['new_password']

        obj = get_user_model().objects.get(pk=id)
        if not obj.check_password(raw_password=password):
            return Response({'error': 'password not match'}, status=400)
        else:
            obj.set_password(new_password)
            obj.save()
            return Response({'success': 'password changed successfully'}, status=200)