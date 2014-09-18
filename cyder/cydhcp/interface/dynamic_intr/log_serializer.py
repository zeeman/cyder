from rest_framework import serializers
from cyder.api.v1.endpoints.dhcp.dynamic_interface.api import \
    DynamicInterfaceNestedAVSerializer
from cyder.cydhcp.interface.dynamic_intr.models import (DynamicInterface,
                                                        DynamicInterfaceAV)


class DynamicInterfaceLogSerializer(serializers.ModelSerializer):
    ctnr = serializers.SlugRelatedField(slug_field='name')
    workgroup = serializers.SlugRelatedField(slug_field='name')
    system = serializers.SerializerMethodField('get_system_representation')
    range = serializers.SerializerMethodField('get_range_representation')
    attributes = DynamicInterfaceNestedAVSerializer(
        source="dynamicinterfaceav_set", many=True)
    modified = serializers.DateTimeField(format='iso-8601')
    last_seen = serializers.DateTimeField(format='iso-8601')
    expire = serializers.DateTimeField(format='iso-8601')
    last_save_user = serializers.SlugRelatedField(slug_field='username')

    class Meta:
        model = DynamicInterface
        fields = ('ctnr', 'workgroup', 'system', 'mac', 'range',
                  'dhcp_enabled', 'last_seen', 'modified', 'expire',
                  'last_save_user')

    def get_system_representation(self, obj):
        return obj.system.audit_repr()
    
    def get_range_representation(self, obj):
        return obj.range.audit_repr()