from django.contrib.auth.models import User
from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase

import cyder
from cyder.base.tests.test_views_template import random_label
from cyder.base.tests.test_views_template import random_byte
from cyder.core.ctnr.models import Ctnr
from cyder.core.cyuser.backends import _has_perm
from cyder.cydns.cname.models import CNAME
from cyder.cydns.address_record.models import AddressRecord
from cyder.cydns.domain.models import Domain
from cyder.cydns.mx.models import MX
from cyder.cydns.ptr.models import PTR
from cyder.cydns.nameserver.models import Nameserver
from cyder.cydns.soa.models import SOA
from cyder.cydns.srv.models import SRV
from cyder.cydns.txt.models import TXT
from cyder.cydns.sshfp.models import SSHFP
from cyder.cydns.tests.utils import create_fake_zone
from cyder.cydns.view.models import View

import json as json

API_VERSION = '1'


def build_sample_domain():
    domain_name = ''
    for i in range(2):
        domain_name = random_label()
        domain = Domain(name=domain_name)
    soa = SOA(primary=random_label(), contact="asf",
              description=random_label())
    soa.save()
    domain.soa = soa
    domain.save()
    return domain


class CydnsAPIAuthTests(object):
    fixtures = ['test_users/test_users.json']
    object_list_url = "/api/v{0}_dns/{1}/"
    object_url = "/api/v{0}_dns/{1}/{2}/"

    def setUp(self):
        super(CydnsAPIAuthTests, self).setUp()
        self.domain = create_fake_zone(random_label(),
                suffix='.oregonstate.edu')

    def test_create_guest(self):
        self.authtest_create("test_guest")

    def test_update_guest(self):
        self.authtest_update("test_guest")

    def test_changing_one_field_guest(self):
        self.authtest_changing_one_field("test_guest")

    def test_delete_guest(self):
        self.authtest_delete("test_guest")

    def test_create_user(self):
        self.authtest_create("test_user")

    def test_update_user(self):
        self.authtest_update("test_user")

    def test_changing_one_field_user(self):
        self.authtest_changing_one_field("test_user")

    def test_delete_user(self):
        self.authtest_delete("test_user")

    def test_create_admin(self):
        self.authtest_create("test_admin")

    def test_update_admin(self):
        self.authtest_update("test_admin")

    def test_changing_one_field_admin(self):
        self.authtest_changing_one_field("test_admin")

    def test_delete_admin(self):
        self.authtest_delete("test_admin")

    def test_create_superuser(self):
        self.authtest_create("test_superuser")

    def test_update_superuser(self):
        self.authtest_update("test_superuser")

    def test_changing_one_field_superuser(self):
        self.authtest_changing_one_field("test_superuser")

    def test_delete_superuser(self):
        self.authtest_delete("test_superuser")

    #Begin helper methods.
    def get_credentials(self, user):
        user_obj = User.objects.get(username=user)
        api_key = ApiKey.objects.get_or_create(user=user_obj)[0].key
        return self.create_apikey(user, api_key)

    def compare_data(self, old_data, new_obj_data):
        for key in old_data.keys():
            self.assertEqual(old_data[key], new_obj_data[key])

    def has_perm(self, user, action):
        user_obj = User.objects.get(username=user)
        return _has_perm(user_obj, Ctnr.objects.get(pk=9999),
                action=action, obj_class=self.test_type)

    def generic_create_auth(self, post_data, user, creds):
        obj_count = self.test_type.objects.count()
        create_url = self.object_list_url.format(
                API_VERSION, str(self.test_type.__name__).lower())
        resp = self.api_client.post(create_url, format='json', data=post_data,
                authentication=creds)
        if self.has_perm(user, cyder.ACTION_CREATE):
            self.assertHttpCreated(resp)
            self.assertEqual(self.test_type.objects.count(), obj_count + 1)
        else:
            self.assertHttpUnauthorized(resp)
            self.assertEqual(self.test_type.objects.count(), obj_count)
        return resp, post_data

    def generic_update_auth(self, patch_url, patch_data, user, creds):
        obj_count = self.test_type.objects.count()
        resp = self.api_client.patch(patch_url, format='json', data=patch_data,
                authentication=creds)
        if self.has_perm(user, cyder.ACTION_UPDATE):
            self.assertHttpAccepted(resp)
            self.assertEqual(self.test_type.objects.count(), obj_count)
        else:
            self.assertHttpUnauthorized(resp)
        return resp, patch_data
    #End helper methods.

    def authtest_create(self, user):
        creds = self.get_credentials(user)
        resp, post_data = self.generic_create_auth(self.post_data(),
                user, creds)
        if self.has_perm(user, cyder.ACTION_CREATE):
            new_object_url = resp.items()[2][1]
            new_resp = self.api_client.get(new_object_url, format='json',
                    authentication=creds)
            self.assertValidJSONResponse(new_resp)
            new_obj_data = json.loads(new_resp.content)
            self.compare_data(post_data, new_obj_data)

    def authtest_update(self, user):
        creds = self.get_credentials(user)
        post_data = self.post_data()
        resp, post_data = self.generic_create_auth(self.post_data(),
                user, creds)
        if self.has_perm(user, cyder.ACTION_UPDATE):
            new_object_url = resp.items()[2][1]
            patch_data = self.post_data()
            update_resp, patch_data = self.generic_update_auth(new_object_url,
                    self.post_data(), user, creds)
            patch_resp = self.api_client.get(new_object_url, format='json',
                    authentication=creds)
            self.assertValidJSONResponse(patch_resp)
            patch_obj_data = json.loads(patch_resp.content)
            self.compare_data(patch_data, patch_obj_data)
        else:
            #TODO: create an object and try to modify it as the user
            super_creds = self.get_credentials("test_superuser")
            resp, post_data = self.generic_create_auth(self.post_data(),
                    "test_superuser", super_creds)
            new_object_url = resp.items()[2][1]
            patch_data = self.post_data()
            update_resp, patch_data = self.generic_update_auth(new_object_url,
                    self.post_data(), user, creds)

    def authtest_changing_one_field(self, user):
        creds = self.get_credentials(user)
        resp, post_data = self.generic_create_auth(self.post_data(),
                user, creds)
        if self.has_perm(user, cyder.ACTION_UPDATE):
            new_object_url = resp.items()[2][1]
            change_post_data = {}
            change_post_data['description'] = "==DIFFERENT=="
            post_data['description'] = "==DIFFERENT=="
            resp, patch_data = self.generic_update_auth(new_object_url,
                    change_post_data, user, creds)
            new_resp = self.api_client.get(new_object_url, format='json',
                    authentication=creds)
            updated_obj_data = json.loads(new_resp.content)
            self.compare_data(post_data, updated_obj_data)

    def authtest_delete(self, user):
        creds = self.get_credentials(user)
        obj_count = self.test_type.objects.count()
        resp, post_data = self.generic_create_auth(self.post_data(),
                user, creds)
        if self.has_perm(user, cyder.ACTION_DELETE):
            new_object_url = resp.items()[2][1]
            self.assertEqual(self.test_type.objects.count(), obj_count + 1)
            resp = self.api_client.delete(new_object_url, format='json',
                    authentication=creds)
            self.assertHttpAccepted(resp)
            self.assertEqual(self.test_type.objects.count(), obj_count)
        else:
            self.assertHttpUnauthorized(resp)
            self.assertEqual(self.test_type.objects.count(), obj_count)


class CNAMEAPITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = CNAME

    def post_data(self):
        test_domain = create_fake_zone(
                random_label(), suffix='.oregonstate.edu')
        test_soa = test_domain.soa
        test_subdomain = Domain.objects.create(
                name=random_label() + '.' + test_domain.name, soa=test_soa)
        return {
            'fqdn': test_subdomain.name,
            'target': random_label(),
            'ttl': 3600,
        }


class MXAPITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = MX

    def post_data(self):
        return {
            'fqdn': 'mxlabel.' + self.domain.name,
            'server': 'mxserver',
            'priority': 123,
            'ttl': 3600,
        }


class SRVAPITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = SRV

    def post_data(self):
        return {
            'description': random_label(),
            'ttl': random_byte(),
            'fqdn': "_" + random_label() + "." + self.domain.name,
            'target': random_label(),
            'priority': 2,
            'weight': 2222,
            'port': 222
        }


class TXTAPITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = TXT

    def post_data(self):
        return {
            'description': random_label(),
            'ttl': random_byte(),
            'fqdn': 'f' + random_label() + "." + self.domain.name,
            'txt_data': random_label()
        }


class NameserverAPITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = Nameserver

    def post_data(self):
        return {
            'server': 'g' + random_label(),
            'description': random_label(),
            'ttl': random_byte(),
            'domain': self.domain.name,
        }


class SSHFPAPITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = SSHFP

    def post_data(self):
        return {
            'description': random_label(),
            'ttl': random_byte(),
            'fqdn': 'h' + random_label() + "." + self.domain.name,
            'algorithm_number': 1,
            'fingerprint_type': 1,
            'key': '9d97e98f8af710c7e7fe703abc8f639e0ee50222'
        }


class AddressRecordV4APITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = AddressRecord

    def post_data(self):
        return {
            'fqdn': self.domain.name,
            'ip_type': '4',
            'ip_str': '196.168.1.2',
            'ttl': random_byte(),
            'description': random_label()
        }


class AddressRecordV6APITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = AddressRecord

    def post_data(self):
        return {
            'description': random_label(),
            'ttl': random_byte(),
            'fqdn': 'j' + random_label() + "." + self.domain.name,
            'ip_str': "1000:{0}:{1}:{2}::".format(random_byte(), random_byte(),
                                                  random_byte()),
            'ip_type': '6'
        }


class PTRV6APITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = PTR

    def setUp(self):
        Domain.objects.get_or_create(name='arpa')
        Domain.objects.get_or_create(name='ip6.arpa')
        Domain.objects.get_or_create(name='1.ip6.arpa')
        super(PTRV6APITests, self).setUp()

    def post_data(self):
        return {
            'description': 'k' + random_label(),
            'ttl': random_byte(),
            'ip_str': "1000:{0}:{1}:{2}:{3}:{4}::".format(
                random_byte(), random_byte(), random_byte(), random_byte(),
                random_byte()),
            'ip_type': '6',
            'name': random_label()
        }


class PTRV4APITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = PTR

    def setUp(self):
        Domain.objects.get_or_create(name='arpa')
        Domain.objects.get_or_create(name='in-addr.arpa')
        Domain.objects.get_or_create(name='11.in-addr.arpa')
        super(PTRV4APITests, self).setUp()

    def post_data(self):
        return {
            'description': random_label(),
            'ttl': random_byte(),
            'ip_str': "11.{0}.{1}.{2}".format(
                random_byte(), random_byte(), random_byte()),
            'ip_type': '4',
            'name': random_label()
        }


"""
Need to hook up system resource before this will work.
class StaticIntrV4APITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = StaticInterface

    def setUp(self):
        Domain.objects.get_or_create(name='arpa')
        Domain.objects.get_or_create(name='in-addr.arpa')
        Domain.objects.get_or_create(name='11.in-addr.arpa')
        super(StaticIntrV4APITests, self).setUp()
        self.s = System(hostname="foobar")
        self.s.save()

    def compare_data(self, old_data, new_obj_data):
        for key in old_data.keys():
            if key == 'system_hostname':
                self.assertEqual(old_data[key],
                                 new_obj_data['system']['hostname'])
                continue
            if key in ('iname', 'system'):
                continue  # StaticInterface needs this done. Too lazy to factor
                          # a comparison function out
            self.assertEqual(old_data[key], new_obj_data[key])

    def test_create_hostname(self):
        post_data = self.post_data()
        del post_data['system']
        post_data['system_hostname'] = self.s.hostname
        resp, post_data = self.generic_create(post_data)
        new_object_url = resp.items()[2][1]
        new_resp = self.api_client.get(new_object_url, format='json')
        self.assertValidJSONResponse(new_resp)
        new_obj_data = json.loads(new_resp.content)
        self.compare_data(post_data, new_obj_data)

    def post_data(self):
        return {
            'description': 'm' + random_label(),
            'ttl': random_byte(),
            'mac': '11:22:33:44:55:00',
            'system': '/tasty/systems/system/{0}/'.format(self.s.pk),
            'fqdn': 'a' + random_label() + "." + self.domain.name,
            'iname': 'eth2.4',
            'dhcp_enabled': False,
            'dns_enabled': True,
            'ip_str': "11.255.{0}.{1}".format(random_byte(), random_byte()),
            'ip_type': '4'
        }


class StaticIntrV6APITests(CydnsAPIAuthTests, ResourceTestCase):
    test_type = StaticInterface

    def setUp(self):
        Domain.objects.get_or_create(name='arpa')
        Domain.objects.get_or_create(name='ip6.arpa')
        Domain.objects.get_or_create(name='2.ip6.arpa')
        super(StaticIntrV6APITests, self).setUp()
        self.s = System(hostname="foobar")
        self.s.save()

    def compare_data(self, old_data, new_obj_data):
        for key in old_data.keys():
            if key == 'iname' or key == 'system':
                continue  # StaticInterface needs this done. Too lazy to factor
                          # a comparison function out
            self.assertEqual(old_data[key], new_obj_data[key])

    def post_data(self):
        return {
            'description': random_label(),
            'ttl': random_byte(),
            'fqdn': 'p' + random_label() + "." + self.domain.name,
            'iname': 'mgmt4',
            'dhcp_enabled': True,
            'dns_enabled': True,
            'mac': '11:22:33:44:55:00',
            'system': '/tasty/systems/system/{0}/'.format(self.s.pk),
            'ip_str': "2000:a{0}:a{1}:a{2}::".format(
                random_byte(), random_byte(), random_byte()),
            'ip_type': '6'
        }
"""
