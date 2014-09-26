from rest_framework import serializers

from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import TXT


class TXTLogSerializer(BaseLogSerializer):
    domain = serializers.SlugRelatedField(slug_field="name")

    class Meta:
        model = TXT
        fields = ('label', 'domain', 'txt_data', 'ttl', 'description', 'ctnr',
                  'last_save_user')
