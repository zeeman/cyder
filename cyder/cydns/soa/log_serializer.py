from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import SOA


class SOALogSerializer(BaseLogSerializer):
    root_domain = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = SOA
        fields = ('ttl', 'primary', 'contact', 'serial', 'expire', 'retry',
                  'refresh', 'minimum', 'description', 'root_domain', 'dirty',
                  'is_signed', 'dns_enabled', 'last_save_user')