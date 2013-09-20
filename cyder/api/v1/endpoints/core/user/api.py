from django.contrib.auth.models import User
from rest_framework import serializers, viewsets

from cyder.api.v1.endpoints.api import NestedFieldSerializer
from cyder.core.cyuser.models import UserProfile


class UserSerializer(NestedFieldSerializer):
    ctnruser_set = serializers.HyperlinkedRelatedField(
        many=True, read_only=False, view_name='api-core-ctnr-detail')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'ctnruser_set', 'is_superuser']
        nested_fields = ['ctnruser_set']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    default_ctnr = serializers.HyperlinkedRelatedField(
        view_name='api-core-ctnr-detail')

    class Meta:
        model = UserProfile
        fields = ['user', 'default_ctnr', 'phone_number']


class UserProfileViewSet(viewsets.ModelViewSet):
    model = UserProfile
    serializer_class = UserProfileSerializer
