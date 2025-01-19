from rest_framework.permissions import BasePermission, SAFE_METHODS
# Change name to permissions_classes.py
class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool((request.method in SAFE_METHODS and request.user and request.user.is_authenticated) or 
                    (request.user and request.user.is_staff))
    

class IsOwnerOrAdmin(BasePermission):
    '''Checks if user is owner or admin'''
    def has_object_permission(self, request, view, obj):
        return bool((request.user == obj.user) or
                    (request.user and request.user.is_staff))