from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.cydhcp.range.models import Range


class RangeLogSerializer(BaseLogSerializer):
    network = serializers.SerializerMethodField('get_network_representation')
    domain = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = Range
        fields = ('network', 'range_type', 'ip_type', 'start_str', 'end_str',
                  'domain', 'is_reserved', 'allow', 'dhcpd_raw_include',
                  'dhcp_enabled', 'name', 'description', 'allow_voip_phones',
                  'range_usage', 'last_save_user')

    def get_network_representation(self, obj):
        return str(obj.network)
