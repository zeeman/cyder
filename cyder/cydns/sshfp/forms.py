from django import forms

from cyder.cydns.forms import DNSForm
from cyder.cydns.sshfp.models import SSHFP
from cyder.base.mixins import UsabilityFormMixin


class SSHFPForm(DNSForm, UsabilityFormMixin):
    class Meta:
        model = SSHFP
        exclude = ('fqdn', 'last_save_user', 'log')
        fields = ('label', 'domain', 'key', 'algorithm_number',
                  'fingerprint_type', 'views', 'ttl', 'description',)
        widgets = {'views': forms.CheckboxSelectMultiple}


class FQDNSSHFPForm(DNSForm):
    class Meta:
        model = SSHFP
        exclude = ('label', 'domain', 'last_save_user', 'log')
        widgets = {'views': forms.CheckboxSelectMultiple}
