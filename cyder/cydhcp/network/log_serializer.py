from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.cydhcp.network.models import Network


class NetworkLogSerializer(BaseLogSerializer):
    vlan = serializers.SlugRelatedField(slug_field='name')
    site = serializers.SlugRelatedField(slug_field='name')
    vrf = serializers.SlugRelatedField(slug_field='name')
    network_address = serializers.CharField(source='network_str')
    dhcp_config_extras = serializers.CharField(source='dhcpd_raw_include')

    class Meta:
        model = Network
        fields = ('vlan', 'site', 'vrf', 'ip_type', 'network_address',
                  'enabled', 'dhcp_config_extras', 'last_save_user')
