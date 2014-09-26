from django.conf.urls.defaults import *

from cyder.cydns.urls import cydns_urls
from cyder.cydns.srv.views import srv_detail


urlpatterns = cydns_urls('srv') + [
    url(r'(?P<pk>[\w-]+)/$', srv_detail, name='srv-detail')]
