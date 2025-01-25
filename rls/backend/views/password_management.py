from backend.serializers import ChangePasswordSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

User = get_user_model()

class ChangePassword(GenericAPIView):

    serializer_class = ChangePasswordSerializer

    def put(self, request, id):
        try: is_admin = request.user.is_staff
        except: is_admin = False
        try: password = request.data['password']
        except: password = ""
        
        new_password = request.data['new_password']
        obj = get_user_model().objects.get(pk=id)
        if is_admin:
            obj.set_password(new_password)
            obj.save()
            return Response({'success': 'password changed successfully'}, status=200)
        
        if not obj.check_password(raw_password=password):
                return Response({'error': 'password not match'}, status=400)
        new_password = request.data['new_password']
        obj.set_password(new_password)
        obj.save()
        return Response({'success': 'password changed successfully'}, status=200)