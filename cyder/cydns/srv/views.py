from cyder.base.views import cy_detail
from cyder.cydns.srv.models import SRV


def srv_detail(request, pk):
    return cy_detail(
        request, SRV, 'cydns/cydns_detail.html', {}, pk=pk)
