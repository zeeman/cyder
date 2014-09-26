from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import SOA


class SOALogSerializer(BaseLogSerializer):
    root_domain = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = SOA
        fields = ('root_domain', 'primary', 'contact', 'expire', 'retry',
                  'refresh', 'minimum', 'ttl', 'description', 'is_signed',
                  'dns_enabled', 'last_save_user')