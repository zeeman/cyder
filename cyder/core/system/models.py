from django.db import models
from django.db.models import Q
from django.db.models.loading import get_model

from cyder.base.eav.models import Attribute, EAVBase
from cyder.base.mixins import ObjectUrlMixin
from cyder.base.models import BaseModel
from cyder.base.helpers import get_display


class System(BaseModel, ObjectUrlMixin):
    name = models.CharField(max_length=255, unique=False)

    search_fields = ('name',)
    display_fields = ('name',)

    def __str__(self):
        return get_display(self)

    class Meta:
        db_table = 'system'

    @staticmethod
    def filter_by_ctnr(ctnr, objects=None):
        objects = objects or System.objects
        DynamicInterface = get_model('dynamic_intr', 'dynamicinterface')
        StaticInterface = get_model('static_intr', 'staticinterface')
        dynamic_query = DynamicInterface.objects.filter(
            ctnr=ctnr).values_list('system')
        static_query = StaticInterface.objects.filter(
            ctnr=ctnr).values_list('system')
        return objects.filter(Q(id__in=static_query) | Q(id__in=dynamic_query))

    def details(self):
        """For tables."""
        data = super(System, self).details()
        data['data'] = [
            ('Name', 'name', self),
        ]
        return data

    @staticmethod
    def eg_metadata():
        """EditableGrid metadata."""
        return {'metadata': [
            {'name': 'name', 'datatype': 'string', 'editable': True},
        ]}


class SystemAV(EAVBase):
    class Meta(EAVBase.Meta):
        db_table = 'system_av'


    entity = models.ForeignKey(System)
    attribute = models.ForeignKey(Attribute)
