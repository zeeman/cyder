from rest_framework import serializers

from cyder.api.v1.endpoints.dns import api
from cyder.core.ctnr.models import Ctnr
from cyder.cydns.domain.models import Domain


class DomainSerializer(serializers.Serializer):
    id = serializers.Field()

    class Meta(api.CommonDNSMeta):
        model = Domain

    def __init__(self, *args, **kwargs):
        super(DomainSerializer, self).__init__(*args, **kwargs)
        master_domain_id = (
            'master_domain' in kwargs['data'] and
            int(kwargs['data']['master_domain'].split('/')[-2])
            or None
        )
        self.master_domain = serializers.HyperlinkedRelatedField(
            many=False, view_name='api-dns-domain-detail',
            queryset=Domain.objects.filter(id=master_domain_id))
        self.ctnr_set = serializers.HyperlinkedRelatedField(
            many=True, view_name='api-core-ctnr-detail',
            queryset=Ctnr.objects.filter(domains__domain=self.object))

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.name = attrs.get('name', instance.name)
            instance.master_domain = (
                'master_domain' in attrs and
                int(attrs['master_domain'].split('/')[-2]) or
                instance.master_domain
            )
            instance.soa = attrs.get('soa', instance.soa)
            instance.is_reverse = attrs.get('is_reverse', instance.is_reverse)
            instance.dirty = attrs.get('dirty', instance.dirty)
            instance.purgeable = attrs.get('purgeable', instance.purgeable)
            instance.delegated = attrs.get('delegated', instance.delegated)
            instance.save()
            for ctnr in attrs.get('ctnr_set', instance.ctnr_set):
                instance.ctnr_set.add(ctnr)
            return instance

        ctnr_set = attrs.pop('ctnr_set', None)
        if 'master_domain' in attrs:
            attrs['master_domain'] = int(
                attrs['master_domain'].split('/')[-2])
        domain = Domain(**attrs)
        domain.save()
        for ctnr in ctnr_set:
            domain.ctnr_set.add(ctnr)
        return Domain


class DomainViewSet(api.CommonDNSViewSet):
    model = Domain
    serializer_class = DomainSerializer
