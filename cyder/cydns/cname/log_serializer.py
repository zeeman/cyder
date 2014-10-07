from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import CNAME


class CNAMELogSerializer(BaseLogSerializer):
    domain = serializers.SlugRelatedField(slug_field="name")
    time_to_live = serializers.IntegerField(source="ttl")

    class Meta:
        model = CNAME
        fields = ('label', 'domain', 'target', 'last_save_user', 'description',
                  'time_to_live')
