from django import forms

from cyder.cydns.forms import DNSForm
from cyder.cydns.srv.models import SRV
from cyder.base.mixins import UsabilityFormMixin


class SRVForm(DNSForm, UsabilityFormMixin):
    class Meta:
        model = SRV
        exclude = ('fqdn', 'last_save_user', 'log')
        fields = ('label', 'domain', 'target', 'port', 'priority', 'weight',
                 'views', 'ttl', 'description')
        widgets = {'views': forms.CheckboxSelectMultiple}


class FQDNSRVForm(DNSForm):
    class Meta:
        model = SRV
        exclude = ('label', 'domain', 'last_save_user', 'log')
        widgets = {'views': forms.CheckboxSelectMultiple}
