from rest_framework import serializers, viewsets

from cyder.api.v1.endpoints.api import (CommonAPINestedAVSerializer,
                                        NestedFieldSerializer)
from cyder.core.system.models import System, SystemAV


class SystemAVSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='id')
    entity = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='api-core-system-detail')
    attribute = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = SystemAV


class SystemAVViewSet(viewsets.ModelViewSet):
    model = SystemAV
    queryset = SystemAV.objects.all()
    serializer_class = SystemAVSerializer


class SystemNestedAVSerializer(CommonAPINestedAVSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='api-core-system_attributes-detail')
    attribute = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = SystemAV
        fields = ['id', 'attribute', 'value']


class SystemSerializer(NestedFieldSerializer):
    systemav_set = SystemNestedAVSerializer(many=True)

    class Meta:
        model = System
        nested_fields = ['systemav_set']


class SystemViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    avmodel = SystemAV
