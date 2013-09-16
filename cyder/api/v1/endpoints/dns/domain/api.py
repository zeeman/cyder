from rest_framework import serializers

from cyder.api.v1.endpoints.dns import api
from cyder.cydns.domain.models import Domain


class DomainSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field()
    master_domain = serializers.HyperlinkedRelatedField(
        many=False, view_name='api-dns-domain-detail')
    ctnr_set = serializers.HyperlinkedRelatedField(
        many=True, view_name='api-core-ctnr-detail')

    class Meta(api.CommonDNSMeta):
        model = Domain


class DomainViewSet(api.CommonDNSViewSet):
    model = Domain
    serializer_class = DomainSerializer
