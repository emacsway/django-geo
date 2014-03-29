from __future__ import absolute_import, unicode_literals
import sys
from django_ext.conf import Settings

LOCATION_ROOT = 1
PATH_SEPARATOR = '/'
PATH_DIGITS = 10

settings = Settings(
    __name__.rsplit('.', 1).pop(0).replace('.', '_').upper(),
    sys.modules[__name__]
)
