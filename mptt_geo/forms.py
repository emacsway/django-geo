from django import forms

from mptt_geo.models import Location, Country, Region, City, Street


class LocationForm(forms.ModelForm):
    """Location form"""

    class Meta:
        model = Location
        exclude = ['creator', 'content_type', 'body', 'parent', 'child_class',
                   'geoname_id', 'geoname_status', ]


class CountryForm(LocationForm):
    """Country form"""

    class Meta:
        model = Country
        exclude = ['creator', 'content_type', 'body', 'parent', 'child_class',
                   'geoname_id', 'geoname_status', ]


class RegionForm(LocationForm):
    """Region form"""

    class Meta:
        model = Region
        exclude = ['creator', 'content_type', 'body', 'parent', 'child_class',
                   'geoname_id', 'geoname_status', ]


class CityForm(LocationForm):
    """City form"""

    class Meta:
        model = City
        exclude = ['creator', 'content_type', 'body', 'parent', 'child_class',
                   'geoname_id', 'geoname_status', ]


class StreetForm(LocationForm):
    """Street form"""

    class Meta:
        model = Street
        exclude = ['creator', 'content_type', 'body', 'parent', 'child_class',
                   'geoname_id', 'geoname_status', ]
