from cyder.base.constants import (LEVEL_GUEST, LEVEL_USER, LEVEL_ADMIN,
                                  ACTION_VIEW, ACTION_UPDATE)
from cyder.base.utils import mixedmethod


def has_perm(self, request, action, obj=None, obj_class=None, ctnr=None):
        return _has_perm(request.user, ctnr or request.session['ctnr'], action,
            obj, obj_class)


def get_user_level(user, ctnr):
    from cyder.core.ctnr.models import CtnrUser
    user_level = None

    # Get user level.
    try:
        ctnr_level = CtnrUser.objects.get(ctnr=ctnr, user=user).level
        is_ctnr_admin = ctnr_level == LEVEL_ADMIN
        is_ctnr_user = ctnr_level == LEVEL_USER
        is_ctnr_guest = ctnr_level == LEVEL_GUEST
    except CtnrUser.DoesNotExist:
        is_ctnr_admin = False
        is_ctnr_user = False
        is_ctnr_guest = False
    try:
        cyder_level = CtnrUser.objects.get(ctnr=1, user=user).level
        is_cyder_admin = cyder_level == LEVEL_ADMIN
        is_cyder_user = cyder_level == LEVEL_USER
        is_cyder_guest = cyder_level == LEVEL_GUEST
    except CtnrUser.DoesNotExist:
        is_cyder_admin = False
        is_cyder_user = False
        is_cyder_guest = False

    if user.is_superuser:
        user_level = 'superuser'
    elif is_cyder_admin:
        user_level = 'cyder_admin'
    elif is_ctnr_admin:
        user_level = 'ctnr_admin'
    elif is_cyder_user or is_ctnr_user:
        user_level = 'user'
    elif is_cyder_guest or is_ctnr_guest:
        user_level = 'guest'
    else:
        user_level = 'pleb'
    return user_level


# Special permissions functions to be passed to the perms factory.
def allow_all(action, *args, **kwargs):
    return True


def read_only(action, *args, **kwargs):
    return action == ACTION_VIEW


def deny(action, *args, **kwargs):
    return False
# End permissions functions.


def custom_has_perm(cyder_admin_perms,
                    ctnr_admin_perms,
                    user_perms=read_only,
                    guest_perms=read_only,
                    pleb_perms=deny,
                    special_case=None):
    """
    This function is a factory for .has_perm methods, designed to greatly
    simplify the process of handling permissions when they follow the standard
    has_perm model.

    Params:
          * cyder_admin_perms, ctnr_admin_perms, user_perms, guest_perms,
            pleb_perms - Must be functions which accept an action constant
            and return True if the action is allowed.
            user_perms, guest_perms default to read_only. pleb_perms defaults to
            deny. This appears consistent with
          * special_case - A callable which is invoked when the user tries to
            access an object. It should accept the object, user, and container.

    If special_case(obj, user, ctnr) returns True and the user's level allows
    them to perform the given action, then
    """

    @mixedmethod
    def inner_has_perm(self, cls, user, ctnr, action):
        """
        Dispatches to appropriate permissions check for user level,
        """
        if user.is_superuser:
            return True

        user_level = get_user_level(user, ctnr)
        perm_handler = {
            "superuser": allow_all,
            "cyder_admin": cyder_admin_perms,
            "ctnr_admin": ctnr_admin_perms,
            "user": user_perms,
            "guest": guest_perms,
            "pleb": pleb_perms,
        }.get(user_level, None)

        if perm_handler is None:
            # The previous _has_perm implementation simply denied access to
            # unhandled user levels. Raising an exception forces user
            # permissions to be well-defined, reducing the risk of unintended
            # behavior.
            raise Exception("No handler for user level {} in {}".format(
                user_level, cls.__name__
            ))

        if (
            # Special case handler.
            #
            self is not None and
            special_case is not None and
            not special_case(self, user, ctnr)
        ):
            return False
        else:  # either self is None or the special case passed
            return perm_handler(action)

    return inner_has_perm


def _has_perm(user, ctnr, action, obj=None, obj_class=None):
    """
    The new _has_perm system is entirely different from the old. Instead of
    having a dispatch table with different handling functions for each Model,
    refactor the handling function into the Model itself. This has a few
    advantages:
        - Models now handle privileges directly, instead of having relevant code
          hidden away in a function the developer has to find.
        - Models that have more complex permissions (such as per-user
          restrictions) can now be supported by _has_perm.
        - We finally don't have to continually refactor _has_perm's complex
          procedural logic.

    This function reproduces the interface and functionality of the old
    _has_perm function in order to minimize the need for immediate refactoring.
    Since pretty much all permissions stuff is currently handled using this
    interface, it will be maintained indefinitely. However, it should be treated
    as deprecated, and code that currently relies on it should be refactored.
    """
    return (obj.has_perm(user, ctnr, action) if obj else
            obj_class.has_perm(user, ctnr, action))