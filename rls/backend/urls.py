from django.urls import include, path
from rest_framework import routers
from tutorial.quickstart import views
from backend.views.viewsets import ContainerViewSet, DeviceViewSet, ReservationViewSet, DeviceTypeViewSet
from backend.views.user_views import SchedulerAvailability

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
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