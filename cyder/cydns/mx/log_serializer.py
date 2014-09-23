from rest_framework import serializers

from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import MX


class MXLogSerializer(BaseLogSerializer):
    class Meta:
        model = MX
        fields = ('fqdn', 'server', 'priority', 'ttl', 'description',
                  'last_save_user')