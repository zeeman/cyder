from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import Nameserver


class NameserverLogSerializer(BaseLogSerializer):
    domain = serializers.SerializerMethodField('domain_repr')
    addr_glue = serializers.SerializerMethodField('addr_glue_repr')
    intr_glue = serializers.SerializerMethodField('intr_glue_repr')

    class Meta:
        model = Nameserver
        fields = ('domain', 'server', 'ttl', 'last_save_user', 'description')

    def addr_glue_repr(self, obj):
        return str(obj.addr_glue)

    def intr_glue_repr(self, obj):
        return str(obj.intr_glue)

    def domain_repr(self, obj):
        return str(obj.domain)