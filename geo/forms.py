from __future__ import absolute_import, unicode_literals
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings

from .models import Location, Country, Region, City, Street

if 'modeltranslation' in settings.INSTALLED_APPS:
    from modeltranslation.translator import translator, NotRegistered
else:
    translator = None

base_exclude = ['content_type', 'active', 'creator', 'body',
                'child_class', 'geoname_id', 'geoname_status', ]

if translator:
    from modeltranslation_ext.forms import TranslationBulkModelForm as ModelForm
else:
    ModelForm = forms.ModelForm


class MetaBase:
    exclude = base_exclude


class LocationForm(ModelForm):
    """Location form"""
    parent = forms.ModelChoiceField(
        queryset=Location.objects.filter(active=True),
        required=True,
        widget=forms.HiddenInput
    )

    class Meta(MetaBase):
        model = Location

    def validate_unique(self):
        """
        Calls the instance's validate_unique() method and updates the form's
        validation errors if any were raised.
        """
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            self._update_errors(e.message_dict)


class CountryForm(LocationForm):
    """Country form"""

    class Meta(MetaBase):
        model = Country


class RegionForm(LocationForm):
    """Region form"""

    class Meta(MetaBase):
        model = Region


class CityForm(LocationForm):
    """City form"""

    class Meta(MetaBase):
        model = City


class StreetForm(LocationForm):
    """Street form"""

    class Meta(MetaBase):
        model = Street
