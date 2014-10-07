from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import SOA


class SOALogSerializer(BaseLogSerializer):
    root_domain = serializers.SlugRelatedField(slug_field='name')
    time_to_live = serializers.IntegerField(source="ttl")

    class Meta:
        model = SOA
        fields = ('root_domain', 'primary', 'contact', 'expire', 'retry',
                  'refresh', 'minimum', 'time_to_live', 'description',
                  'is_signed', 'dns_enabled', 'last_save_user')