from cyder.base.views import cy_detail
from cyder.cydns.txt.models import TXT


def txt_detail(request, pk):
    return cy_detail(
        request, TXT, 'cydns/cydns_detail.html', {}, pk=pk)
