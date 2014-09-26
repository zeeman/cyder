from cyder.base.views import cy_detail
from cyder.cydns.mx.models import MX


def mx_detail(request, pk):
    return cy_detail(request, MX, 'cydns/cydns_detail.html', {}, pk=pk)