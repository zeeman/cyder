from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import SSHFP


class SSHFPLogSerializer(BaseLogSerializer):
    ctnr = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = SSHFP
        fields = ('label', 'domain', 'key', 'algorithm_number',
                  'fingerprint_type', 'ttl', 'description', 'ctnr',
                  'last_save_user')