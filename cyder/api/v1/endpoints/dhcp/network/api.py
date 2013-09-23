from rest_framework import serializers

from cyder.api.v1.endpoints.api import NestedFieldSerializer
from cyder.api.v1.endpoints.dhcp import api
from cyder.cydhcp.network.models import Network, NetworkKeyValue


class NetworkKeyValueSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='id')
    network = serializers.HyperlinkedRelatedField(
        view_name='api-dhcp-network-detail')

    class Meta:
        model = NetworkKeyValue


class NetworkKeyValueViewSet(api.CommonDHCPViewSet):
    model = NetworkKeyValue
    serializer_class = NetworkKeyValueSerializer


class NetworkNestedKeyValueSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='api-dhcp-network_keyvalues-detail')

    class Meta:
        model = NetworkKeyValue
        fields = api.NestedKeyValueFields


class NetworkSerializer(NestedFieldSerializer):
    vlan = serializers.HyperlinkedRelatedField(
        view_name='api-dhcp-vlan-detail')
    site = serializers.HyperlinkedRelatedField(
        view_name='api-dhcp-site-detail')
    vrf = serializers.HyperlinkedRelatedField(
        view_name='api-dhcp-vrf-detail')
    networkkeyvalue_set = NetworkNestedKeyValueSerializer(many=True)

    class Meta(api.CommonDHCPMeta):
        model = Network
        depth = 1
        nested_fields = ['networkkeyvalue_set']


class NetworkViewSet(api.CommonDHCPViewSet):
    model = Network
    serializer_class = NetworkSerializer
    keyvaluemodel = NetworkKeyValue
