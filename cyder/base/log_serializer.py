from rest_framework import serializers


class BaseLogSerializer(serializers.ModelSerializer):
    last_save_user = serializers.SlugRelatedField(slug_field="username")


class ExpirableLogMixin(object):
    expire = serializers.DateTimeField(format="%m/%d/%Y")