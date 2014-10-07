from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import SSHFP


class SSHFPLogSerializer(BaseLogSerializer):
    ctnr = serializers.SlugRelatedField(slug_field='name')
    time_to_live = serializers.IntegerField(source="ttl")

    class Meta:
        model = SSHFP
        fields = ('label', 'domain', 'key', 'algorithm_number',
                  'fingerprint_type', 'time_to_live', 'description', 'ctnr',
                  'last_save_user')