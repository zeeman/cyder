from django import forms

from cyder.base.eav.forms import get_eav_form
from cyder.cydhcp.vlan.models import Vlan, VlanAV


class VlanForm(forms.ModelForm):
    #site = forms.ModelChoiceField(queryset=Site.objects.all())

    class Meta:
        model = Vlan
        exclude = 'last_save_user', 'log'


VlanAVForm = get_eav_form(VlanAV, Vlan)
