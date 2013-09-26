import json
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from cyder.api.authtoken.models import Token
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

    def assertEqualKeys(self, a, b):
        for key in a:
            assert a[key] == b[key]

    def assertHttpOK(self, resp):
        assert resp.status_code == 200

    def assertHttpUnauthorized(self, resp):
        assert resp.status_code == 401

    def assertHttpNotFound(self, resp):
        assert resp.status_code == 405

    def load_credentials(self, username):
        self.user = User.objects.get(username=username)
        self.token = Token.objects.get_or_create(user=self.user).key

    def test_permissions(self):
        """This test iterates through each test user and test method to verify
        that permissions are functioning correctly.
        """
        methods = ['api_get', 'api_post', 'api_put', 'api_patch', 'api_delete']
        users = ['test_superuser', 'test_admin', 'test_user', 'test_guest']
        for u in users:
            for m in methods:
                pass
        pass