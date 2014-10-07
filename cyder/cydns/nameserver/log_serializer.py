from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import Nameserver


class NameserverLogSerializer(BaseLogSerializer):
    domain = serializers.SlugRelatedField(slug_field="name")
    time_to_live = serializers.IntegerField(source="ttl")

    class Meta:
        model = Nameserver
        fields = ('domain', 'server', 'time_to_live', 'last_save_user',
                  'description')
