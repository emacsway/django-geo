from django.core.exceptions import ImproperlyConfigured
from django.db.models import signals, get_app
from django.utils.translation import ugettext_noop as _
from . import models
from .models import Location

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
    from . import settings
    try:
        Location.objects.get(pk=settings.LOCATION_ROOT)
    except Location.DoesNotExist:
        root = Location(**{
            'parent': None,
            'name': 'Location',
            'name_ascii': 'Location',
            'active': True,
        })
        root.save()
        settings.CATEGORY_ROOT = root.pk

signals.post_syncdb.connect(create_root_node, sender=models)
