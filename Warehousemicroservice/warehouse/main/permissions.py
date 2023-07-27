from rest_framework.permissions import BasePermission

class IsReadOnlyOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            # Allow any authenticated user to have read-write permissions
            return True
        # Otherwise, only allow safe (read-only) methods for unauthenticated users
        return request.method in ('GET', 'HEAD', 'OPTIONS')
