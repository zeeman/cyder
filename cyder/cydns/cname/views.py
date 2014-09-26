from cyder.base.views import cy_detail
from cyder.cydns.cname.models import CNAME


def cname_detail(request, pk):
    return cy_detail(
        request, CNAME, 'cydns/cydns_detail.html', {}, pk=pk)