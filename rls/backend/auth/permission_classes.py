from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import User


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool((request.method in SAFE_METHODS and request.user and request.user.is_authenticated) or 
                    (request.user and request.user.is_staff))
    

class IsOwnerOrAdmin(BasePermission):
    '''Checks if user is owner or admin'''
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            owner = obj
        else:
            owner = obj.user
        return bool((request.user == owner) or
                    (request.user and request.user.is_staff))