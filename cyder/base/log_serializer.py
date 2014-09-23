from rest_framework import serializers


class BaseLogSerializer(serializers.ModelSerializer):
    last_save_user = serializers.SlugRelatedField(slug_field="username")