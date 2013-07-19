from tastypie.authorization import Authorization

import cyder
from cyder.core.cyuser.backends import _has_perm
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
        }[string.lower()]

    def is_authorized(self, request, object=None):
        if request.user.is_superuser:
            return True

        action = {
            'POST': cyder.ACTION_CREATE,
            'GET': cyder.ACTION_VIEW,
            'PATCH': cyder.ACTION_UPDATE,
            'DELETE': cyder.ACTION_DELETE,
        }[request.META['REQUEST_METHOD']]

        user_obj = request.user
        for ctnruser_obj in user_obj.ctnruser_set.all():
            ctnr = ctnruser_obj.ctnr
            obj_class = self.str_to_class(
                    request.META['PATH_INFO'].split('/')[3])
            if _has_perm(user_obj, ctnr, action, obj_class=obj_class):
                return True

        return False
