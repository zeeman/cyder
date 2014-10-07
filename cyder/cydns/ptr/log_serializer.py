from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import PTR


class PTRLogSerializer(BaseLogSerializer):
    ip_address = serializers.CharField(source="ip_str")
    time_to_live = serializers.IntegerField(source="ttl")

    class Meta:
        model = PTR
        fields = 'ip_address', 'fqdn', 'time_to_live', 'last_save_user'
