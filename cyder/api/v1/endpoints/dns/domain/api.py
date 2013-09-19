from rest_framework import serializers

from cyder.api.v1.endpoints.api import NestedFieldSerializer
from cyder.api.v1.endpoints.dns import api
from cyder.cydns.domain.models import Domain


class DomainSerializer(NestedFieldSerializer):
    id = serializers.Field(source='id')
    master_domain = serializers.HyperlinkedRelatedField(
        many=False, read_only=False, view_name='api-dns-domain-detail')
    ctnr_set = serializers.HyperlinkedRelatedField(
        many=True, read_only=False, view_name='api-core-ctnr-detail')

    class Meta(api.CommonDNSMeta):
        model = Domain
        nested_fields = ['ctnr_set']


class DomainViewSet(api.CommonDNSViewSet):
    model = Domain
    serializer_class = DomainSerializer
