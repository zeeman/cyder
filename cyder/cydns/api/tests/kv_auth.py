import json

from django.contrib.auth.models import User
from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase

import cyder
from cyder.base.tests.test_views_template import random_byte
from cyder.base.tests.test_views_template import random_label
from cyder.core.ctnr.models import Ctnr
from cyder.core.cyuser.backends import _has_perm
from cyder.core.system.models import System
from cyder.cydhcp.interface.static_intr.models import StaticInterface
from cyder.cydns.domain.models import Domain
from cyder.cydns.tests.utils import create_fake_zone

API_VERSION = 1


class KVAPIAuthTests(object):
    fixtures = ['test_users/test_users.json']
    object_list_url = "/api/v{0}_dns/{1}/"
    object_url = "/api/v{0}_dns/{1}/{2}/"

    def setUp(self):
        super(KVAPIAuthTests, self).setUp()
        self.domain = create_fake_zone(
            random_label(), suffix='.oregonstate.edu')

    def test_create_guest(self):
        self.authtest_create("test_guest")

    def test_update_guest(self):
        self.authtest_update("test_guest")

    def test_delete_guest(self):
        self.authtest_delete("test_guest")

    def test_create_user(self):
        self.authtest_create("test_user")

    def test_update_user(self):
        self.authtest_update("test_user")

    def test_delete_user(self):
        self.authtest_delete("test_user")

    def test_create_admin(self):
        self.authtest_create("test_admin")

    def test_update_admin(self):
        self.authtest_update("test_admin")

    def test_delete_admin(self):
        self.authtest_delete("test_admin")

    def test_create_superuser(self):
        self.authtest_create("test_superuser")

    def test_update_superuser(self):
        self.authtest_update("test_superuser")

    def test_delete_superuser(self):
        self.authtest_delete("test_superuser")

    #Start helper functions.
    def get_credentials(self, user):
        user_obj = User.objects.get(username=user)
        api_key = ApiKey.objects.get_or_create(user=user_obj)[0].key
        return self.create_apikey(user, api_key)

    def compare_data(self, old_data, new_obj_data):
        for key in old_data:
            self.assertEqual(old_data[key], new_obj_data[key])

    def has_perm(self, user, action):
        user_obj = User.objects.get(username=user)
        return _has_perm(user_obj, Ctnr.objects.get(pk=9999), action=action,
                         obj_class=self.test_type)

    def generic_create_auth(self, post_data, user, creds):
        obj_count = self.test_type.objects.count()
        create_url = self.object_list_url.format(
            API_VERSION, str(self.test_type.__name__).lower())
        resp = self.api_client.post(
            create_url, format='json', data=post_data, authentication=creds)
        if self.has_perm(user, cyder.ACTION_CREATE):
            self.assertHttpCreated(resp)
            self.assertEqual(self.test_type.objects.count(), obj_count + 1)
        else:
            self.assertHttpUnauthorized(resp)
            self.assertEqual(self.test_type.objects.count(), obj_count)
        return resp, post_data

    def generic_update_auth(self, patch_url, patch_data, user, creds):
        obj_count = self.test_type.objects.count()
        resp = self.api_client.patch(
            patch_url, format='json', data=patch_data, authentication=creds)
        if self.has_perm(user, cyder.ACTION_UPDATE):
            self.assertHttpAccepted(resp)
            self.assertEqual(self.test_type.objects.count(), obj_count)
        else:
            self.assertHttpUnauthorized(resp)
        return resp, patch_data
    #End helper functions.

    def authtest_create(self, user):
        #create record with superuser
        super_creds = self.get_credentials("test_superuser")
        post_data = self.setup_data()
        self.generic_create_auth(
                self.setup_data(), "test_superuser", super_creds)

        #create new kv pair using test user
        creds = self.get_credentials(user)
        resp, post_data = self.generic_create_auth(
            self.post_data(), user, creds)
        if self.has_perm(user, cyder.ACTION_CREATE):
            new_object_url = resp.items()[2][1]
            new_resp = self.api_client.get(
                new_object_url, format='json', authentication=creds)
            self.assertValidJSONResponse(new_resp)
            new_obj_data = json.loads(new_resp.content)
            self.compare_data(post_data, new_obj_data)

    def authtest_update(self, user):
        creds = self.get_credentials(user)
        resp, post_data = self.generic_create_auth(
            self.setup_data(), user, creds)
        if self.has_perm(user, cyder.ACTION_UPDATE):
            new_object_url = resp.items()[2][1]
            update_resp, patch_data = self.generic_update_auth(
                new_object_url, self.post_data(), user, creds)
            patch_resp = self.api_client.get(
                new_object_url, format='json', authentication=creds)
            self.assertValidJSONResponse(patch_resp)
            patch_obj_data = json.loads(patch_resp.content)
            self.compare_data(patch_data, patch_obj_data)
        else:
            super_creds = self.get_credentials("test_superuser")
            resp, post_data = self.generic_create_auth(
                self.post_data(), "test_superuser", super_creds)
            new_object_url = resp.items()[2][1]
            patch_data = self.post_data()
            update_resp, patch_data = self.generic_update_auth(
                new_object_url, self.post_data(), user, creds)

    def authtest_delete(self, user):
        creds = self.get_credentials(user)
        obj_count = self.test_type.objects.count()
        resp, post_data = self.generic_create_auth(
            self.setup_data(), user, creds)
        if self.has_perm(user, cyder.ACTION_DELETE):
            new_object_url = resp.items()[2][1]
            self.assertEqual(self.test_type.objects.count(), obj_count + 1)
            resp = self.api_client.delete(
                new_object_url, format='json', authentication=creds)
            self.assertHttpAccepted(resp)
            self.assertEqual(self.test_type.objects.count(), obj_count)
        else:
            self.assertHttpUnauthorized(resp)
            self.assertEqual(self.test_type.objects.count(), obj_count)

    def test_bad_value_create(self):
        creds = self.get_credentials("test_superuser")
        post_data = self.bad_post_data()
        obj_count = self.test_type.objects.count()
        create_url = self.object_list_url.format(
            API_VERSION, str(self.test_type.__name__).lower())
        resp = self.api_client.post(
            create_url, format='json', data=post_data, authentication=creds)
        self.assertHttpBadRequest(resp)
        self.assertEqual(self.test_type.objects.count(), obj_count)

    def test_bad_value_update(self):
        creds = self.get_credentials("test_superuser")
        good_post_data = self.setup_data()
        resp, post_data = self.generic_create_auth(
            good_post_data, "test_superuser", creds)
        self.assertHttpCreated(resp)
        new_object_url = resp.items()[2][1]
        resp = self.api_client.patch(new_object_url, format='json',
                                     data=self.bad_post_data(),
                                     authentication=creds)
        self.assertHttpBadRequest(resp)
        new_resp = self.api_client.get(
            new_object_url, format='json', authentication=creds)
        self.assertValidJSONResponse(new_resp)
        new_obj_data = json.loads(new_resp.content)
        assert "interface_type" not in new_obj_data


class StaticIntrKVAPITests(KVAPIAuthTests, ResourceTestCase):
    test_type = StaticInterface

    def setUp(self):
        Domain.objects.get_or_create(name='arpa')
        Domain.objects.get_or_create(name='in-addr.arpa')
        Domain.objects.get_or_create(name='11.in-addr.arpa')
        super(StaticIntrKVAPITests, self).setUp()
        self.s = System(name="foobar")
        self.s.save()

    def setup_data(self):
        return {
            'description': 'm' + random_label(),
            'ttl': random_byte(),
            'mac': '11:22:33:44:55:00',
            'system': self.object_url.format(API_VERSION, 'system', self.s.pk),
            'fqdn': 'a' + random_label() + '.' + self.domain.name,
            'iname': 'eth2.4',
            'dhcp_enabled': False,
            'dns_enabled': True,
            'ip_str': "11.255.{0}.{1}".format(random_byte(), random_byte()),
            'ip_type': '4'
        }

    def post_data(self):
        return {
            'key': random_label(),
            'value': random_label()
        }

    def bad_post_data(self):
        return {
            'key': 'interface_type',
            'value': 'kajfl'
        }

    def good_post_data(self):
        return {
            'key': 'interface_type',
            'value': 'eth'
        }
