from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import SSHFP


class SSHFPLogSerializer(BaseLogSerializer):
    class Meta:
        model = SSHFP
        fields = ('fqdn', 'key', 'algorithm_number', 'fingerprint_type',
                  'last_save_user')