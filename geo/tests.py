from __future__ import absolute_import, unicode_literals
from django.conf import settings as dsettings
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.test import TestCase

from . import settings
from .models import Location
from .forms import CountryForm

if 'modeltranslation_ext' in dsettings.INSTALLED_APPS:
    from modeltranslation_ext.utils import localize_fieldname
else:
    localize_fieldname = lambda x: x


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
            CountryForm().fields[localize_fieldname('name')].label
        )

    def test_add(self):
        response = self.client.post(
            urlresolvers.reverse(
                'geo_location_detail',
                kwargs={'pk': settings.LOCATION_ROOT, }
            ), {localize_fieldname('name'): 'Ukraine',
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
            CountryForm().fields[localize_fieldname('name')].label
        )

    def test_add(self):
        response = self.client.post(
            urlresolvers.reverse(
                'geo_location_detail',
                kwargs={'pk': settings.LOCATION_ROOT, }
            ), {localize_fieldname('name'): 'Ukraine',
                'name_ascii': 'Ukraine',
                'iso_alpha2': 'UK',
                'iso_alpha3': 'UKR',
            }
        )
        self.assertEqual(response.status_code, 302)
        """
        self.assertContains(
            response,
            'Ukraine',
        )
        """

    def test_admin_index(self):
        response = self.client.get(urlresolvers.reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            urlresolvers.reverse('admin:geo_location_changelist')
        )
        self.assertContains(
            response,
            urlresolvers.reverse('admin:geo_location_add')
        )

        self.assertContains(
            response,
            urlresolvers.reverse('admin:geo_country_changelist')
        )
        self.assertContains(
            response,
            urlresolvers.reverse('admin:geo_country_add')
        )

        self.assertContains(
            response,
            urlresolvers.reverse('admin:geo_region_changelist')
        )
        self.assertContains(
            response,
            urlresolvers.reverse('admin:geo_region_add')
        )

        self.assertContains(
            response,
            urlresolvers.reverse('admin:geo_city_changelist')
        )
        self.assertContains(
            response,
            urlresolvers.reverse('admin:geo_city_add')
        )

        self.assertContains(
            response,
            urlresolvers.reverse('admin:geo_street_changelist')
        )
        self.assertContains(
            response,
            urlresolvers.reverse('admin:geo_street_add')
        )

    def test_admin_location_add(self):
        response = self.client.get(
            urlresolvers.reverse('admin:geo_location_add')
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="creator"')

    def test_admin_country_add(self):
        response = self.client.get(
            urlresolvers.reverse('admin:geo_country_add')
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="creator"')

    def test_admin_region_add(self):
        response = self.client.get(
            urlresolvers.reverse('admin:geo_region_add')
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="creator"')

    def test_admin_city_add(self):
        response = self.client.get(
            urlresolvers.reverse('admin:geo_city_add')
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="creator"')

    def test_admin_street_add(self):
        response = self.client.get(
            urlresolvers.reverse('admin:geo_street_add')
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="creator"')
