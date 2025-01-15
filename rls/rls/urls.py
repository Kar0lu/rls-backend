from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include('backend.auth.urls')),
    path('api/', include('backend.urls'))
]