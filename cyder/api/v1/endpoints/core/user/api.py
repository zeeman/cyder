from django.contrib.auth.models import User
from rest_framework import serializers, viewsets

from cyder.core.cyuser.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    ctnruser_set = serializers.HyperlinkedRelatedField(
        many=True, view_name='api-core-ctnr-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'ctnruser_set', 'is_superuser']


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
