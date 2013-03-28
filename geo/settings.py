from __future__ import absolute_import, unicode_literals
from django.conf import settings
from .models import Location

LOCATION_ROOT = getattr(
    settings,
    'GEO_LOCATION_ROOT',
    1
)
