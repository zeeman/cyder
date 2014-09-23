from rest_framework import serializers
from cyder.base.log_serializer import BaseLogSerializer
from cyder.models import Vlan


class VlanLogSerializer(BaseLogSerializer):
    class Meta:
        model = Vlan
        fields = "name", "number", "last_save_user"
