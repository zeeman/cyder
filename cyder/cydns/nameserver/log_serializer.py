from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import Nameserver


class NameserverLogSerializer(BaseLogSerializer):
    domain = serializers.SlugRelatedField(slug_field="name")

    class Meta:
        model = Nameserver
        fields = ('domain', 'server', 'ttl', 'last_save_user', 'description')
