from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import DynamicInterface


class DynamicInterfaceLogSerializer(BaseLogSerializer):
    ctnr = serializers.SlugRelatedField(slug_field='name')
    workgroup = serializers.SlugRelatedField(slug_field='name')
    system = serializers.SlugRelatedField(slug_field='name')
    range = serializers.SerializerMethodField('get_range_representation')
    last_save_user = serializers.SlugRelatedField(slug_field='username')

    class Meta:
        model = DynamicInterface
        fields = ('ctnr', 'workgroup', 'system', 'mac', 'range',
                  'dhcp_enabled', 'last_seen', 'modified', 'expire',
                  'last_save_user')
    
    def get_range_representation(self, obj):
        return obj.range.audit_repr()