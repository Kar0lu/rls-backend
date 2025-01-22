from django.urls import include, path
from rest_framework import routers
from backend.views.viewsets import ContainerViewSet, DeviceViewSet, ReservationViewSet, DeviceTypeViewSet, UserViewSet, CreateUser
from backend.views.availability import SchedulerAvailability
from backend.views.user_reservability import UserReservability

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'containers', ContainerViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'deviceTypes', DeviceTypeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('availability/', SchedulerAvailability.as_view()),
    path('reservability/<int:user_id>/', UserReservability.as_view()),
    path('reservability/', UserReservability.as_view()),
    path('register/', CreateUser.as_view()),
]