from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import signals, get_app
from django.utils.translation import ugettext_noop as _
from . import models
from .models import Location

LOCATION_ROOT = getattr(settings, 'GEO_LOCATION_ROOT', 1)

try:
    notification = get_app('notification')

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type(
            "geo_location_new",
            _("Added a new geo location"),
            _("a new geo location has been created"),
            default=1
        )

    signals.post_syncdb.connect(create_notice_types, sender=notification)
except ImproperlyConfigured:
    print "Skipping creation of NoticeTypes as notification app not found"


def create_root_node(app, created_models, verbosity, **kwargs):
    try:
        Location.objects.get(pk=LOCATION_ROOT)
    except Location.DoesNotExist:
        Location(**{
            'id': LOCATION_ROOT,
            'parent': None,
            'name': 'Location',
            'name_ascii': 'Location',
            'active': True,
        }).save()

signals.post_syncdb.connect(create_root_node, sender=models)
