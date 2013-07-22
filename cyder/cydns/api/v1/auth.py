from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

import cyder
from cyder.core.cyuser.backends import _has_perm
from cyder.cydhcp.interface.static_intr.models import StaticInterface
from cyder.cydns.address_record.models import AddressRecord
from cyder.cydns.cname.models import CNAME
from cyder.cydns.domain.models import Domain
from cyder.cydns.mx.models import MX
from cyder.cydns.nameserver.models import Nameserver
from cyder.cydns.ptr.models import PTR
from cyder.cydns.soa.models import SOA
from cyder.cydns.srv.models import SRV
from cyder.cydns.sshfp.models import SSHFP
from cyder.cydns.txt.models import TXT


class CyderAuthorization(Authorization):
    """Checks if user has access to the requested object via any of their
    assigned containers.
    """

    def str_to_class(self, string):
        return {
            'addressrecord': AddressRecord,
            'cname': CNAME,
            'domain': Domain,
            'mx': MX,
            'nameserver': Nameserver,
            'ptr': PTR,
            'soa': SOA,
            'srv': SRV,
            'sshfp': SSHFP,
            'txt': TXT,
            'staticinterface': StaticInterface,
        }[string.lower()]

    def has_perm_list(self, object_list, bundle, action, error_msg):
        user_obj = bundle.request.user
        for obj in object_list:
            obj_class = obj.__class__
            for ctnruser_obj in user_obj.ctnruser_set.all():
                ctnr_obj = ctnruser_obj.ctnr
                if _has_perm(user_obj, ctnr_obj, action, obj_class=obj_class):
                    return True
            else:
                raise Unauthorized(error_msg.format(repr(obj)))

    def has_perm_detail(self, object_list, bundle, action, error_msg):
        user_obj = bundle.request.user
        obj_class = bundle.obj.__class__
        for ctnruser_obj in user_obj.ctnruser_set.all():
            ctnr_obj = ctnruser_obj.ctnr
            if _has_perm(user_obj, ctnr_obj, action, obj_class=obj_class):
                return True
        else:
            raise Unauthorized(error_msg.format(repr(bundle.obj)))

    def read_list(self, object_list, bundle):
        return self.has_perm_list(
            object_list, bundle, cyder.ACTION_VIEW,
            "You may not view the record {0}.")

    def read_detail(self, object_list, bundle):
        return self.has_perm_detail(
            object_list, bundle, cyder.ACTION_VIEW,
            "You may not view the record {0}.")

    def create_list(self, object_list, bundle):
        return self.has_perm_list(
            object_list, bundle, cyder.ACTION_CREATE,
            "You may not create the record {0}.")

    def create_detail(self, object_list, bundle):
        return self.has_perm_detail(
            object_list, bundle, cyder.ACTION_CREATE,
            "You may not create the record {0}.")

    def update_list(self, object_list, bundle):
        return self.has_perm_list(
            object_list, bundle, cyder.ACTION_UPDATE,
            "You may not update the record {0}.")

    def update_detail(self, object_list, bundle):
        return self.has_perm_detail(
            object_list, bundle, cyder.ACTION_UPDATE,
            "You may not update the record {0}.")

    def delete_list(self, object_list, bundle):
        return self.has_perm_list(
            object_list, bundle, cyder.ACTION_DELETE,
            "You may not delete the record {0}")

    def delete_detail(self, object_list, bundle):
        return self.has_perm_detail(
            object_list, bundle, cyder.ACTION_DELETE,
            "You may not delete the record {0}.")
