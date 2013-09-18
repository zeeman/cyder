from rest_framework import serializers

from cyder.api.v1.endpoints.dns import api
from cyder.cydns.domain.models import Domain


class DomainSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='id')
    master_domain = serializers.HyperlinkedRelatedField(
        many=False, read_only=False, view_name='api-dns-domain-detail')
    ctnr_set = serializers.HyperlinkedRelatedField(
        many=True, read_only=False, view_name='api-core-ctnr-detail')

    def restore_object(self, attrs, instance=None):
        if not self.is_valid():
            return self.errors

        if instance is not None:
            if 'ctnr_set' in attrs:
                ctnr_set = attrs.pop('ctnr_set')
                for c in ctnr_set:
                    self.instance.ctnr_set.add(c)
            for field in self.fields:
                setattr(instance, field, attrs.get(
                    field, getattr(instance, field)))
            instance.save()

        ctnr_set = attrs.pop('ctnr_set', None)
        d = Domain(**attrs)
        d.save()
        if ctnr_set:
            for c in ctnr_set:
                d.ctnr_set.add(c)

    # Looks like we need to override save_object() and full_clean() to make
    # this work. Otherwise, when DRF tries to save() it screws up the process.

    class Meta(api.CommonDNSMeta):
        model = Domain


class DomainViewSet(api.CommonDNSViewSet):
    model = Domain
    serializer_class = DomainSerializer
