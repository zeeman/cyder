import json

from django.contrib.auth.models import User
from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase

import cyder
from cyder.base.tests.test_views_template import random_label
from cyder.core.ctnr.models import Ctnr
from cyder.core.cyuser.backends import _has_perm
from cyder.cydhcp.interface.static_intr.models import StaticInterface

API_VERSION = 1

class KVAPIAuthTests(object):
    fixtures = ['test_users/test_users.json']
    object_list_url = "/api/v{0}_dns/{1}/"
    object_url = "/api/v{0}_dns/{1}/{2}/"

    def setUp(self):
        super(KVAPIAuthTests, self).setUp()

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
        return _has_perm(user_obj, Ctnr.objects.get(pk=9999),
                action=action, obj_class=self.test_type)

    def generic_create_auth(self, post_data, user, creds):
        obj_count = self.test_type.objects.count()
        create_url = self.object_list_url.format(
                API_VERSION, str(self.test_type.__name__).lower())
        resp = self.api_client.post(create_url, format='json', data=post_data,
                authentication=creds)
        import pdb; pdb.set_trace()
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
    #End helper functions.

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
        resp, post_data = self.generic_create_auth(self.post_data(),
                user, creds)
        if self.has_perm(user, cyder.ACTION_UPDATE):
            new_object_url = resp.items()[2][1]
            update_resp, patch_data = self.generic_update_auth(new_object_url,
                    self.post_data(), user, creds)
            patch_resp = self.api_client.get(new_object_url, format='json',
                    authentication=creds)
            self.assertValidJSONResponse(patch_resp)
            patch_obj_data = json.loads(patch_resp.content)
            self.compare_data(patch_data, patch_obj_data)
        else:
            super_creds = self.get_credentials("test_superuser")
            resp, post_data = self.generic_create_auth(self.post_data(),
                    "test_superuser", super_creds)
            new_object_url = resp.items()[2][1]
            patch_data = self.post_data()
            update_resp, patch_data = self.generic_update_auth(new_object_url,
                    self.post_data(), user, creds)

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

    def test_bad_value_create(self):
        creds = self.get_credentials("test_superuser")
        post_data = self.bad_post_data()
        obj_count = self.test_type.objects.count()
        create_url = self.object_list_url.format(
                API_VERSION, str(self.test_type.__name__).lower())
        resp = self.api_client.post(create_url, format='json', data=post_data,
                authentication=creds)
        self.assertHttpBadRequest(resp)
        self.assertEqual(self.test_type.objects.count(), obj_count)

    def test_bad_value_update(self):
        creds = self.get_credentials("test_superuser")
        good_post_data = self.good_post_data()
        resp, post_data = self.generic_create_auth(good_post_data,
                "test_superuser", creds)
        self.assertHttpCreated(resp)
        new_object_url = resp.items()[2][1]
        resp = self.api_client.patch(new_object_url, format='json',
                data=self.bad_post_data(), authentication=creds)
        self.assertHttpBadRequest(resp)
        new_resp = self.api_client.get(new_object_url, format='json',
                authentication=creds)
        self.assertValidJSONResponse(new_resp)
        new_obj_data = json.loads(new_resp.content)
        self.assertEqual(good_post_data, new_obj_data)

class StaticIntrKVAPITests(KVAPIAuthTests, ResourceTestCase):
    test_type = StaticInterface

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
