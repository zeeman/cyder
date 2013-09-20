from rest_framework import serializers

from cyder.api.v1.endpoints.api import NestedFieldSerializer
from cyder.api.v1.endpoints.dhcp import api
from cyder.cydhcp.range.models import Range, RangeKeyValue


class RangeKeyValueSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='id')
    range = serializers.HyperlinkedRelatedField(
        view_name='api-dhcp-range-detail')

    class Meta:
        model = RangeKeyValue


class RangeKeyValueViewSet(api.CommonDHCPViewSet):
    model = RangeKeyValue
    serializer_class = RangeKeyValueSerializer


class RangeNestedKeyValueSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='api-dhcp-range_keyvalues-detail')

    class Meta:
        model = RangeKeyValue
        fields = api.NestedKeyValueFields


class RangeSerializer(NestedFieldSerializer):
    rangekeyvalue_set = RangeNestedKeyValueSerializer(many=True)
    ctnr_set = serializers.HyperlinkedRelatedField(
        many=True, read_only=False, view_name='api-core-ctnr-detail')

    class Meta(api.CommonDHCPMeta):
        model = Range
        depth = 1
        nested_fields = ['ctnr_set']


class RangeViewSet(api.CommonDHCPViewSet):
    model = Range
    serializer_class = RangeSerializer
