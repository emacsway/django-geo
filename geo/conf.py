from __future__ import absolute_import, unicode_literals
import sys
from django.conf import settings as django_settings

LOCATION_ROOT = 1
PATH_SEPARATOR = '/'
PATH_DIGITS = 10


class Settings(object):
    prefix = __name__.rsplit('.', 1).pop(0).replace('.', '_').upper()
    settings = django_settings
    defaults = sys.modules[__name__]

    def __getattr__(self, name):
        try:
            return getattr(self.settings, '_'.join((self.prefix, name)))
        except AttributeError:
            try:
                return getattr(self.defaults, name)
            except AttributeError:
                return getattr(self.settings, name)

    def __dir__(self):
        return dir(self.defaults) + dir(self.settings)

settings = Settings()
