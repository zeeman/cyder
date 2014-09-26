from django.conf.urls.defaults import *

from cyder.cydns.urls import cydns_urls
from cyder.cydns.mx.views import mx_detail


urlpatterns = cydns_urls('mx') + [
    url(r'(?P<pk>[\w-]+)/$', mx_detail, name='mx-detail')]
