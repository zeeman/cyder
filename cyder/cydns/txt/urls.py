from django.conf.urls.defaults import *

from cyder.cydns.urls import cydns_urls
from cyder.cydns.txt.views import txt_detail


urlpatterns = cydns_urls('txt') + [
    url(r'(?P<pk>[\w-]+)/$', txt_detail, name='txt-detail')]
