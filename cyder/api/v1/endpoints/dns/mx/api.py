from rest_framework import serializers

from cyder.api.v1.endpoints.dns import api
from cyder.cydns.mx.models import MX


class MXSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    domain = serializers.HyperlinkedRelatedField(
        many=False, view_name='api-dns-domain-detail')
    views = serializers.SlugRelatedField(
        many=True, slug_field='name')

    class Meta(api.CommonDNSMeta):
        model = MX


class MXViewSet(api.CommonDNSViewSet):
    model = MX
    serializer_class = MXSerializer
