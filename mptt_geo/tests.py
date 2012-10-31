from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.test import TestCase

from . import settings
from .models import Location
from .forms import CountryForm


class GeoForUserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             email="test@mailinator.com",
                                             password="testpwd")
        response = self.client.login(username='test', password='testpwd')
        self.assertTrue(response)

    def test_root(self):
        response = self.client.get(
            urlresolvers.reverse(
                'geo_location_detail',
                kwargs={'pk': settings.LOCATION_ROOT, }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            Location.objects.get(pk=settings.LOCATION_ROOT).name
        )
        self.assertNotContains(
            response,
            CountryForm().fields['name'].label
        )

    def test_add(self):
        response = self.client.post(
            urlresolvers.reverse(
                'geo_location_detail',
                kwargs={'pk': settings.LOCATION_ROOT, }
            ), {'name': 'Ukraine',
                'name_ascii': 'Ukraine',
                'iso_alpha2': 'UK',
                'iso_alpha3': 'UKR',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response,
            'Ukraine',
        )


class GeoAdminTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin',
                                             email="admin@mailinator.com",
                                             password="adminpwd")
        response = self.client.login(username='admin', password='adminpwd')
        self.assertTrue(response)

    def test_root(self):
        response = self.client.get(
            urlresolvers.reverse(
                'geo_location_detail',
                kwargs={'pk': settings.LOCATION_ROOT, }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            Location.objects.get(pk=settings.LOCATION_ROOT).name
        )
        self.assertContains(
            response,
            CountryForm().fields['name'].label
        )

    def test_add(self):
        response = self.client.post(
            urlresolvers.reverse(
                'geo_location_detail',
                kwargs={'pk': settings.LOCATION_ROOT, }
            ), {'name': 'Ukraine',
                'name_ascii': 'Ukraine',
                'iso_alpha2': 'UK',
                'iso_alpha3': 'UKR',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Ukraine',
        )
