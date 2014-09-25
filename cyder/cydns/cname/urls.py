from django.conf.urls.defaults import *

from cyder.cydns.urls import cydns_urls
from cyder.cydns.cname.views import cname_detail


urlpatterns = cydns_urls('cname') + patterns(
    '',
    url(r'(?P<pk>[\w-]+)/$', cname_detail, name='cname-detail'),
)
