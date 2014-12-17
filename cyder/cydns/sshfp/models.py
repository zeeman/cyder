import re
from gettext import gettext as _

from django.db import models
from django.core.exceptions import ValidationError

from cyder.base.models import LoggedModel
from cyder.base.utils import safe_save
from cyder.cydns.models import CydnsRecord, LabelDomainMixin


def validate_algorithm(number):
    if number not in (1, 2):
        raise ValidationError(
            "Algorithm number must be with 1 (RSA) or 2 (DSA)")


def validate_fingerprint(number):
    if number not in (1,):
        raise ValidationError("Fingerprint type must be 1 (SHA-1)")


is_sha1 = re.compile("[0-9a-fA-F]{40}")


def validate_sha1(sha1):
    if not is_sha1.match(sha1):
        raise ValidationError("Invalid key.")


class SSHFP(LoggedModel, LabelDomainMixin, CydnsRecord):
    """
    >>> SSHFP(label=label, domain=domain, key=key_data,
    ... algorithm_number=algo_num, fingerprint_type=fing_type)
    """

    pretty_type = 'SSHFP'

    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=256, validators=[validate_sha1])
    algorithm_number = models.PositiveIntegerField(
        null=False, blank=False, validators=[validate_algorithm],
        help_text="Algorithm number must be with 1 (RSA) or 2 (DSA)")
    fingerprint_type = models.PositiveIntegerField(
        null=False, blank=False, validators=[validate_fingerprint],
        help_text="Fingerprint type must be 1 (SHA-1)")

    template = _("{bind_name:$lhs_just} {ttl:$ttl_just}  "
                 "{rdclass:$rdclass_just} "
                 "{rdtype:$rdtype_just} {algorithm_number} {fingerprint_type} "
                 "{key:$rhs_just}")

    search_fields = ("fqdn", "key")

    class Meta:
        app_label = 'cyder'
        db_table = 'sshfp'
        unique_together = ('domain', 'label')
        # TODO
        # _mysql_exceptions.OperationalError: (1170, "BLOB/TEXT column
        # 'txt_data' used in key specification without a key length")
        # Fix that ^

    def serializer(self):
        from cyder.cydns.sshfp.log_serializer import SSHFPLogSerializer
        return SSHFPLogSerializer(self)

    def details(self):
        """For tables."""
        data = super(SSHFP, self).details()
        data['data'] = [
            ('Label', 'label', self.label),
            ('Domain', 'domain', self.domain),
            ('Algorithm', 'algorithm_number', self.algorithm_number),
            ('Fingerprint Type', 'fingerprint_type', self.fingerprint_type),
            ('Key', 'key', self.key),
        ]
        return data

    @staticmethod
    def eg_metadata():
        """EditableGrid metadata."""
        return {'metadata': [
            {'name': 'label', 'datatype': 'string', 'editable': True},
            {'name': 'domain', 'datatype': 'string', 'editable': True},
            {'name': 'algorithm', 'datatype': 'integer', 'editable': True},
            {'name': 'fingerprint_type', 'datatype': 'integer',
             'editable': True},
            {'name': 'key', 'datatype': 'string', 'editable': True},
        ]}

    @property
    def rdtype(self):
        return 'SSHFP'

    @safe_save
    def save(self, *args, **kwargs):
        super(SSHFP, self).save(*args, **kwargs)
