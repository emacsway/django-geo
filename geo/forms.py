from __future__ import absolute_import, unicode_literals
from django import forms
from django.conf import settings

from .models import Location, Country, Region, City, Street

if 'modeltranslation' in settings.INSTALLED_APPS:
    from modeltranslation.translator import translator, NotRegistered
else:
    translator = None

base_exclude = ['content_type', 'parent', 'active', 'creator', 'body',
                'child_class', 'geoname_id', 'geoname_status', ]

if translator:
    try:
        trans_opts = translator.get_options_for_model(Location)
    except NotRegistered:
        pass
    else:
        if 'body' in trans_opts.fields:
            base_exclude += [i.name for i in trans_opts.fields['body']]
        from modeltranslation_ext.forms import TranslationBulkModelForm as ModelForm
else:
    ModelForm = forms.ModelForm


class MetaBase:
    exclude = base_exclude


class LocationForm(ModelForm):
    """Location form"""

    class Meta(MetaBase):
        model = Location


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
