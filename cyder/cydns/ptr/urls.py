from django.conf.urls.defaults import *

from cyder.cydns.urls import cydns_urls
from cyder.cydns.ptr.views import ptr_detail


urlpatterns = cydns_urls('ptr') + [
    url(r'(?P<pk>[\w-]+)/$', ptr_detail, name='ptr-detail')]
