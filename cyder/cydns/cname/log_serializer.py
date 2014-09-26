from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import CNAME


class CNAMELogSerializer(BaseLogSerializer):
    domain = serializers.SlugRelatedField(slug_field="name")

    class Meta:
        model = CNAME
        fields = ('label', 'domain', 'target', 'last_save_user', 'description',
                  'ttl')