from django.conf.urls.defaults import *

from cyder.cydns.urls import cydns_urls
from cyder.cydns.sshfp.views import sshfp_detail


urlpatterns = cydns_urls('sshfp') + [
    url(r'(?P<pk>[\w-]+)/$', sshfp_detail, name='sshfp-detail')]
