from rest_framework import serializers, viewsets

import cyder.api.v1.endpoints.core.system.api as system_api
from cyder.api.v1.endpoints.dhcp.static_interface.api import \
    StaticInterfaceSerializer
from cyder.api.v1.endpoints.dhcp.dynamic_interface.api import \
    DynamicInterfaceSerializer
from cyder.core.system.models import System, SystemAV


class StaticInterfaceNestedSerializer(StaticInterfaceSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='api-dhcp-staticinterface-detail')


class DynamicInterfaceNestedSerializer(DynamicInterfaceSerializer):
    id = serializers.HyperlinkedIdentityField(
        view_name='api-dhcp-dynamicinterface-detail')


class InterfaceSerializer(system_api.SystemSerializer):
    staticinterface_set = StaticInterfaceNestedSerializer()
    dynamicinterface_set = DynamicInterfaceNestedSerializer()

    class Meta:
        model = System


class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = InterfaceSerializer
    avmodel = SystemAV
