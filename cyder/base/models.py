import datetime
import simplejson as json
from django.contrib.auth.models import User
from django.core import serializers
from django.db import models
from django.utils.safestring import mark_safe

from rest_framework.renderers import JSONRenderer

from cyder.base.utils import classproperty, dict_diff
from cyder.settings.local import MAX_LOG_ENTRIES

class DeleteLog(models.Model):
    obj_type = models.CharField(max_length=30)
    deleted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    log = models.TextField()


class LoggedModel(models.Model):
    """Allows changes to objects to be logged for auditing purposes.

    Objects inheriting from this class must specify an attribute audit_fields
    listing the names of fields to be logged as strings.

    On deletion, a LoggedModel object will cause the creation of a DeleteLog
    entry, which will record the deleted object's class name, date of deletion,
    and the data contained in the deleted object's log.
    """
    log = models.TextField(blank=True)
    last_save_user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        abstract = True

    def serializer(self):
        raise NotImplementedError("This model inherits from LoggedModel, but "
                                  "it doesn't specify a serializer to use")

    def serialized(self, old):
        data = self.serializer().data
        old_data = old.serializer().data
        changes = dict_diff(old_data, data)

        # these keys will be stored at the top level of the dict, so they
        # don't need to be reproduced in the list of changes
        changes.pop('last_save_user', None)
        changes.pop('modified', None)

        return JSONRenderer().render({
            'last_save_user': data['last_save_user'],
            'modified': datetime.datetime.now(),
            'changes': changes
        })

    def save(self, *args, **kwargs):
        # only update the log if the record has already been saved
        if self.pk:
            old_data = self.__class__.objects.get(pk=self.pk)
            log_lines = self.log.split('\n')

            # get the serialized representation, prepend it to the log
            log_lines.insert(0, self.serialized(old_data))

            # remove log entries if we're over the limit
            if len(log_lines) > MAX_LOG_ENTRIES:
                log_lines = log_lines[:MAX_LOG_ENTRIES]

            self.log = '\n'.join(log_lines)

        return super(LoggedModel, self).save(*args, **kwargs)

    def delete(self, user=None, *args, **kwargs):
        # before deleting, save the data to the DeleteLog
        dl = DeleteLog(obj_type=self.__class__.__name__,
                       log=self.log + "\n" + self.serialized(),
                       user=user)
        dl.save()
        return super(LoggedModel, self).delete(*args, **kwargs)

class BaseModel(models.Model):
    """
    Base class for models to abstract some common features.

    * Adds automatic created and modified fields to the model.
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        get_latest_by = 'created'

    @classproperty
    @classmethod
    def pretty_type(cls):
        return cls.__name__.lower()

    @property
    def pretty_name(self):
        return unicode(self)

    def unique_error_message(self, model_class, unique_check):
        error = super(BaseModel, self).unique_error_message(
            model_class, unique_check)
        kwargs = {}
        for field in unique_check:
            kwargs[field] = getattr(self, field)

        obj = model_class.objects.filter(**kwargs)
        if obj and hasattr(obj.get(), 'get_detail_url'):
            error = error[:-1] + ' at <a href={0}>{1}.</a>'.format(
                obj.get().get_detail_url(), obj.get())
            error = mark_safe(error)
        return error


class ExpirableMixin(models.Model):
    expire = models.DateTimeField(null=True, blank=True,
                                  help_text='Format: MM/DD/YYYY')

    class Meta:
        abstract = True
