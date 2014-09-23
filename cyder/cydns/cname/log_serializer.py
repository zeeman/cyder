from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import CNAME


class CNAMELogSerializer(BaseLogSerializer):
    class Meta:
        model = CNAME
        fields = ('fqdn', 'target', 'last_save_user')