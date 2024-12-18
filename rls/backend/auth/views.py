from django.http import JsonResponse
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

def get_routes(request):
   routes = [
       '/api/token',
       '/api/token/refresh'
   ]
   return JsonResponse(routes, safe=False)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer