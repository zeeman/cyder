from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import PTR


class PTRLogSerializer(BaseLogSerializer):
    ip_address = serializers.CharField(source="ip_str")

    class Meta:
        model = PTR
        fields = 'ip_address', 'fqdn', 'ttl', 'last_save_user'
