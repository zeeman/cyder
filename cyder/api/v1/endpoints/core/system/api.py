from rest_framework import serializers, viewsets

from cyder.api.v1.endpoints.api import NestedFieldSerializer
from cyder.core.system.models import System, SystemKeyValue


class SystemKeyValueSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='id')
    system = serializers.HyperlinkedRelatedField(
        view_name='api-core-system-detail')

    class Meta:
        model = SystemKeyValue


class SystemKeyValueViewSet(viewsets.ModelViewSet):
    model = SystemKeyValue
    queryset = SystemKeyValue.objects.all()
    serializer_class = SystemKeyValueSerializer


class SystemNestedKeyValueSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='api-core-system_keyvalues-detail')

    class Meta:
        model = SystemKeyValue
        fields = ['id', 'key', 'value', 'is_quoted']


class SystemSerializer(NestedFieldSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='api-core-system-detail')
    systemkeyvalue_set = SystemNestedKeyValueSerializer(many=True)

    class Meta:
        model = System
        nested_fields = ['systemkeyvalue_set']


class SystemViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    keyvaluemodel = SystemKeyValue
