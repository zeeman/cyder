from rest_framework import serializers

from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import TXT


class TXTLogSerializer(BaseLogSerializer):
    domain = serializers.SlugRelatedField(slug_field="name")
    time_to_live = serializers.IntegerField(source="ttl")

    class Meta:
        model = TXT
        fields = ('label', 'domain', 'txt_data', 'time_to_live', 'description',
                  'ctnr', 'last_save_user')
