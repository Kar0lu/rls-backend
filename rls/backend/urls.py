from django.urls import include, path
from rest_framework import routers
from tutorial.quickstart import views
from backend.views import ContainerViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'containers', ContainerViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]