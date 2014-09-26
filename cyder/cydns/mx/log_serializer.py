from rest_framework import serializers

from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import MX


class MXLogSerializer(BaseLogSerializer):
    domain = serializers.SlugRelatedField(slug_field="name")

    class Meta:
        model = MX
        fields = ('label', 'domain', 'server', 'priority', 'ttl', 'description',
                  'last_save_user')