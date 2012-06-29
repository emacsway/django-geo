from django import forms

from mptt_geo.models import Location, Country, Region, City, Street


class LocationForm(forms.ModelForm):
    """Location form"""

    class Meta:
        model = Location
        exclude = ['creator', 'content_type', 'body', 'parent', 'geoname_id', ]


class CountryForm(LocationForm):
    """Country form"""

    class Meta:
        model = Country
        exclude = ['creator', 'content_type', 'body', 'parent', 'geoname_id', ]


class RegionForm(LocationForm):
    """Region form"""

    class Meta:
        model = Region
        exclude = ['creator', 'content_type', 'body', 'parent', 'geoname_id', ]


class CityForm(LocationForm):
    """City form"""

    class Meta:
        model = City
        exclude = ['creator', 'content_type', 'body', 'parent', 'geoname_id', ]


class StreetForm(LocationForm):
    """Street form"""

    class Meta:
        model = Street
        exclude = ['creator', 'content_type', 'body', 'parent', 'geoname_id', ]
