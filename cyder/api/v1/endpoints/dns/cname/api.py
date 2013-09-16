from rest_framework import serializers

from cyder.api.v1.endpoints.dns import api
from cyder.cydns.cname.models import CNAME


class CNAMESerializer(api.CommonDNSSerializer, api.FQDNMixin):
    label = serializers.CharField()
    domain = serializers.HyperlinkedRelatedField(
        many=False, view_name='api-dns-domain-detail')

    class Meta(api.CommonDNSMeta):
        model = CNAME


class CNAMEViewSet(api.CommonDNSViewSet):
    model = CNAME
    serializer_class = CNAMESerializer
