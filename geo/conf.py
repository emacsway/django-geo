from __future__ import absolute_import, unicode_literals
from django.conf import settings

LOCATION_ROOT = getattr(
    settings,
    'GEO_LOCATION_ROOT',
    1
)

PATH_SEPARATOR = getattr(settings, 'GEO_PATH_SEPARATOR', '/')
PATH_DIGITS = getattr(settings, 'GEO_PATH_DIGITS', 10)
