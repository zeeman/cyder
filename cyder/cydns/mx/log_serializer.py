from rest_framework import serializers

from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import MX


class MXLogSerializer(BaseLogSerializer):
    domain = serializers.SlugRelatedField(slug_field="name")
    time_to_live = serializers.IntegerField(source="ttl")

    class Meta:
        model = MX
        fields = ('label', 'domain', 'server', 'priority', 'time_to_live',
                  'description', 'last_save_user')