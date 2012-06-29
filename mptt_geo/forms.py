from django import forms
from django.db import transaction
from django.db.models import Q
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

from tree_select.fields import TreeChoiceField

from mptt_geo.models import Location, Country, Region, City, Street


class LocationForm(forms.ModelForm):
    """Location form"""

    class Meta:
        model = Location
        exclude = ['creator', 'content_type', 'body', 'parent', ]


class CountryForm(LocationForm):
    """Country form"""

    class Meta:
        model = Country
        exclude = ['creator', 'content_type', 'body', 'parent', ]


class RegionForm(LocationForm):
    """Region form"""

    class Meta:
        model = Region
        exclude = ['creator', 'content_type', 'body', 'parent', ]


class CityForm(LocationForm):
    """City form"""

    class Meta:
        model = City
        exclude = ['creator', 'content_type', 'body', 'parent', ]


class StreetForm(LocationForm):
    """Street form"""

    class Meta:
        model = Street
        exclude = ['creator', 'content_type', 'body', 'parent', ]
