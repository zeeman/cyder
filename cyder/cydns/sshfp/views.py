from cyder.base.views import cy_detail
from cyder.cydns.sshfp.models import SSHFP


def sshfp_detail(request, pk):
    return cy_detail(
        request, SSHFP, 'cydns/cydns_detail.html', {}, pk=pk)
