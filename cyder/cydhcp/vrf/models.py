from django.db import models
# Create your models here.
from cyder.base.mixins import ObjectUrlMixin
from cyder.cydhcp.network.models import Network
from cyder.cydhcp.keyvalue.models import KeyValue


class Vrf(models.Model, ObjectUrlMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    network = models.ForeignKey(Network, null=True)

    class Meta:
        db_table = 'vrf_class'

    def __str__(self):
        return "Vrf {0} for {1}".format(self.name, self.network)

class VrfKeyValue(KeyValue):
    vrf = models. ForeignKey(Vrf, null=False)

    class Meta:
        db_table = "vrf_key_value"

    def _aa_decription(self):
        return