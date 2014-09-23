from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import TXT


class TXTLogSerializer(BaseLogSerializer):
    class Meta:
        model = TXT
        fields = 'fqdn', 'txt_data', 'last_save_user'