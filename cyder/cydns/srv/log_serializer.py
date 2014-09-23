from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import SRV


class SRVLogSerializer(BaseLogSerializer):
    class Meta:
        model = SRV
        fields = ('fqdn', 'target', 'port', 'priority', 'weight')