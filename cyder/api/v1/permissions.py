from rest_framework import permissions

from cyder.base.constants import (ACTION_VIEW, ACTION_UPDATE, ACTION_DELETE,
                                  ACTION_CREATE)
from cyder.core.cyuser.backends import _has_perm


class ReadOnlyIfAuthenticated(permissions.IsAuthenticated):
    """Basic class to allow only read access."""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated() and
                request.method in permissions.SAFE_METHODS)


method_map = {
    'GET': ACTION_VIEW,
    'OPTIONS': ACTION_VIEW,
    'HEAD': ACTION_VIEW,
    'POST': ACTION_CREATE,
    'PUT': ACTION_UPDATE,
    'PATCH': ACTION_UPDATE,
    'DELETE': ACTION_DELETE
}


class CyderPermissions(permissions.BasePermission):
    """This class implements permissions based on Cyder's permissions model."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

        if (request.user.is_superuser or
                request.method in permissions.SAFE_METHODS):
            return True

        for ctnr in request.user.ctnruser_set.all():
            if _has_perm(request.user, ctnr, method_map[request.method]):
                return True

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated():
            return False

        if (request.user.is_superuser or
                request.method in permissions.SAFE_METHODS):
            return True

        for ctnr in request.user.ctnruser_set.all():
            if _has_perm(request.user, ctnr, method_map[request.method],
                         obj, view.queryset.model):
                return True

        return False