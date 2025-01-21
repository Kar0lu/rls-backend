from django.urls import include, path
from rest_framework import routers
from backend.views.viewsets import ContainerViewSet, DeviceViewSet, ReservationViewSet, DeviceTypeViewSet, UserViewSet
from backend.views.availability import SchedulerAvailability

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
]