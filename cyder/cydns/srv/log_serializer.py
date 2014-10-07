from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import SRV


class SRVLogSerializer(BaseLogSerializer):
    ctnr = serializers.SlugRelatedField(slug_field='name')
    domain = serializers.SlugRelatedField(slug_field="name")
    time_to_live = serializers.IntegerField(source="ttl")

    class Meta:
        model = SRV
        fields = ('label', 'domain', 'target', 'port', 'priority', 'weight',
                  'time_to_live', 'description', 'ctnr', 'last_save_user')