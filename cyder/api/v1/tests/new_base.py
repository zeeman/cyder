import json
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from cyder.api.authtoken.models import Token
from cyder.base.constants import (ACTION_CREATE, ACTION_DELETE, ACTION_UPDATE,
                                  ACTION_VIEW)
from cyder.core.ctnr.models import Ctnr
from cyder.core.cyuser.backends import _has_perm
from cyder.cydns.domain.models import Domain
from cyder.cydns.nameserver.models import Nameserver
from cyder.cydns.soa.models import SOA
from cyder.cydns.view.models import View


API_VERSION = '1'


def build_sample_domain():
    """Build SOA, domain, view, and nameserver records for test objects."""
    soa, _ = SOA.objects.get_or_create(
        primary="ns1.oregonstate.edu", contact="hostmaster.oregonstate.edu",
        description="Test SOA")
    domain, _ = Domain.objects.get_or_create(name="domain", soa=soa)
    view, _ = View.objects.get_or_create(name='test')
    nameserver, _ = Nameserver.objects.get_or_create(
        domain=domain, server="ns1.oregonstate.edu", ttl=3600)
    nameserver.views.add(view)
    domain.views.add(view)
    return domain, view


def build_domain(label, domain_obj):
    """Create a domain from a label and a domain instance."""
    fqdn = ".".join((label, domain_obj.name))
    domain, _ = Domain.objects.get_or_create(
        name=fqdn, soa=domain_obj.soa)
    return domain


class APIKVTestMixin(object):
    """Mixin to test endpoints with key-value support."""
    def __init__(self, *args, **kwargs):
        super(APIKVTestMixin, self).__init__(*args, **kwargs)
        if not hasattr(self, "keyvalue_attr"):
            self.keyvalue_attr = self.model.__name__.lower() + "keyvalue_set"

    def test_keyvalue_read(self):
        obj = self.create_object()
        getattr(obj, self.keyvalue_attr).get_or_create(
            key='Test Key', value='Test Value')
        resp = self.http_get(self.object_url(obj.id))


class APITests(object):
    """Base class for API tests."""
    fixtures = ['test_users/test_users.json']

    client = APIClient()

    f_root_url = "/api/v{0}/"
    f_object_list_url = "/api/v{0}/{1}/{2}/"
    f_object_url = "/api/v{0}/{1}/{2}/{3}/"

    def __init__(self, *args, **kwargs):
        urlname = (
            getattr(self, 'urlname', False) or str(self.model.__name__).lower())

        root = getattr(self, 'root')

        self.domain, self.view = build_sample_domain()

        self.root_url = self.f_root_url.format(API_VERSION)
        self.object_list_url = self.f_object_list_url.format(
            API_VERSION, root, urlname)
        self.object_url = lambda slug: self.f_object_url.format(
            API_VERSION, root, urlname, slug)

    # ABSTRACT FUNCTIONS
    def generate_related_data(self):
        """This method should return a dict of tuples of form
            (Related Object Model, Related Object Data)
        """
        pass

    def generate_data(self):
        """This method should return a dict representing core object data."""
        pass

    def create_related_objects(self):
        """Creates related objects from generate_related_data."""
        pass

    def create_object(self):
        """Creates core object from generate_data and create_related_objects."""
        pass
    # END ABSTRACT FUNCTIONS

    @staticmethod
    def assertEqualKeys(a, b):
        for key in a:
            assert a[key] == b[key]

    @staticmethod
    def assertHttpOK(resp):
        assert resp.status_code == 200

    @staticmethod
    def assertHttpUnauthorized(resp):
        assert resp.status_code == 401

    @staticmethod
    def assertHttpNotFound(resp):
        assert resp.status_code == 404

    @staticmethod
    def assertHttpMethodNotAllowed(resp):
        assert resp.status_code == 405

    def has_perm(self, user, action):
        if not isinstance(user, User):
            user_obj = User.objects.get(username=user)
        return _has_perm(
            user_obj,
            Ctnr.objects.get(pk__in=user_obj.ctnruser_set.
                             values_list('ctnr', flat=True)),
            action,
            obj_class=self.model)

    def load_credentials(self, username):
        self.user = User.objects.get(username=username)
        self.token = Token.objects.get_or_create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_permissions(self):
        """This test iterates through each test user and test method to verify
        that permissions are functioning correctly.
        """
        methods = ['api_get_nonexistent', 'api_get_existing', 'api_get_root',
                   'api_get_list', 'api_get_detail', 'api_post_valid',
                   'api_post_invalid', 'api_put_valid', 'api_put_invalid',
                   'api_patch_valid', 'api_patch_invalid', 'api_delete']
        users = ['test_superuser', 'test_admin', 'test_user', 'test_guest']
        for u in users:
            self.load_credentials(u)
            for m in methods:
                getattr(self, m).description = "{0} as {1}".format(m, u)
                yield getattr(self, m)()

    def api_get_nonexistent(self):
        obj = self.create_object()
        bad_id = obj.id
        obj.delete()
        resp = self.client.get(self.object_url(bad_id))
        (self.has_perm(self.user, ACTION_VIEW)
            and self.assertHttpNotFound(resp)
            or self.assertHttpUnauthorized(resp))

    def api_get_existing(self):
        obj = self.create_object()
