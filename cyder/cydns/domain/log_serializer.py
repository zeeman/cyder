from rest_framework import serializers

from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import Domain


class DomainLogSerializer(BaseLogSerializer):
    master_domain = serializers.SlugRelatedField(slug_field='name')
    soa = serializers.SerializerMethodField('get_soa_representation')

    class Meta:
        model = Domain
        fields = ('name', 'master_domain', 'soa', 'is_reverse', 'dirty',
                  'purgeable', 'delegated', 'last_save_user')

    def get_soa_representation(self, obj):
        return str(obj.soa)