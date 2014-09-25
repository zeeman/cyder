from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import AddressRecord


class AddressRecordLogSerializer(BaseLogSerializer):
    views = serializers.SlugRelatedField(many=True, slug_field='name')

    class Meta:
        model = AddressRecord
        fields = ("fqdn", "ip_str", "last_save_user", "ttl", "description",
                  "views")
