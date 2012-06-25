from django import forms
from django.db import transaction
from django.db.models import Q
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

from tree_select.fields import TreeChoiceField

from mptt_geo.models import Location, Country, Region, City, Street


class LocationForm(forms.ModelForm):
    """Location form"""

    parent = TreeChoiceField('mptt_geo', 'Location', multiple=False,
                             label=_('Parent node'))

    class Meta:
        model = Location
        exclude = ['creator', 'content_type', 'body', ]


class CountryForm(LocationForm):
    """Country form"""

    class Meta:
        model = Country
        exclude = ['creator', 'content_type', 'body', ]


class RegionForm(LocationForm):
    """Region form"""

    class Meta:
        model = Region
        exclude = ['creator', 'content_type', 'body', ]


class CityForm(LocationForm):
    """City form"""

    class Meta:
        model = City
        exclude = ['creator', 'content_type', 'body', ]


class StreetForm(LocationForm):
    """Street form"""

    class Meta:
        model = Street
        exclude = ['creator', 'content_type', 'body', ]
