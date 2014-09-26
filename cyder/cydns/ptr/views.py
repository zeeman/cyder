from cyder.base.views import cy_detail
from cyder.cydns.ptr.models import PTR


def ptr_detail(request, pk):
    return cy_detail(
        request, PTR, 'cydns/cydns_detail.html', {}, pk=pk)
