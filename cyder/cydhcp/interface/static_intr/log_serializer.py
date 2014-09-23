from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import StaticInterface


class StaticInterfaceLogSerializer(BaseLogSerializer):
    ctnr = serializers.SlugRelatedField(slug_field='name')
    reverse_domain = serializers.SlugRelatedField(slug_field='name')
    system = serializers.SlugRelatedField(slug_field='name')
    workgroup = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = StaticInterface
        fields = ('ctnr', 'mac', 'reverse_domain', 'system', 'workgroup',
                  'dhcp_enabled', 'dns_enabled', 'last_seen', 'ip_str',
                  'last_save_user')