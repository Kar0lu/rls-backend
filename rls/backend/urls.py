from django.urls import include, path
from rest_framework import routers
from backend.views.viewsets import (ContainerViewSet,
                                    DeviceViewSet,
                                    ReservationViewSet,
                                    DeviceTypeViewSet,
                                    UserViewSet,
                                    CreateUser)
from backend.views.availability import SchedulerAvailability
from backend.views.hours_left import HoursLeft
from backend.views.files import ListFilesView, RetrieveFileView
from backend.views.list_user_reservations import ListUserReservations
from backend.views.password_management import ChangePassword

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'containers', ContainerViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'deviceTypes', DeviceTypeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('availability/', SchedulerAvailability.as_view()),
    path('user/<int:user_id>/hoursLeft/', HoursLeft.as_view()),
    path('user/hoursLeft/', HoursLeft.as_view()),
    path('register/', CreateUser.as_view()),
    path('user/files/', ListFilesView.as_view()),
    path('user/file/', RetrieveFileView.as_view()),
    path('user/reservations/', ListUserReservations.as_view()),
    path('changePassword/<int:id>/', ChangePassword.as_view()),
]