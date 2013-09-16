from rest_framework import permissions

import cyder
from cyder.api.authtoken.models import Token as CyderToken
from cyder.core.cyuser.backends import _has_perm


class ReadOnlyIfAuthenticated(permissions.IsAuthenticated):
    """Simple permissions class for read-only API use."""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated() and
                request.method in permissions.SAFE_METHODS)

class CyderAuthorization(permissions.BasePermission):
    """Cyder-specific permissions class to allow users to modify site data."""
    def has_permission(self, request, view):
        if not isinstance(request.auth, CyderToken):
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if not isinstance(request.auth, CyderToken):
            return False

        if request.user.is_superuser:
            return True

        action = {
            'POST': cyder.ACTION_CREATE,
            'GET': cyder.ACTION_VIEW,
            'PATCH': cyder.ACTION_UPDATE,
            'PUT': cyder.ACTION_UPDATE,
            'DELETE': cyder.ACTION_DELETE,
            'OPTIONS': cyder.ACTION_VIEW,
        }[request.META['REQUEST_METHOD']]

        ctnruser_set = request.user.ctnruser_set.all()

        for ctnruser in ctnruser_set:
            if _has_perm(request.user, ctnruser.ctnr, action,
                         obj_class=obj.__class__):
                return True

        return False
