from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import PTR


class PTRLogSerializer(BaseLogSerializer):
    class Meta:
        model = PTR
        fields = 'ip_str', 'fqdn', 'ttl', 'last_save_user'
