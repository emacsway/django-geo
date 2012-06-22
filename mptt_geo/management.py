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
        notification.create_notice_type("geo_classified_new", 
                                        _("Geo classified new item"), 
                                        _("a new geo classified item has been created"), 
                                        default=1)
        
    signals.post_syncdb.connect(create_notice_types, sender=notification)
except ImproperlyConfigured:
    print "Skipping creation of NoticeTypes as notification app not found"


def create_root_node(app, created_models, verbosity, **kwargs):
    try:
        Location.objects.get(pk=LOCATION_ROOT)
    except Location.DoesNotExist:
        Location.objects.create(**{
            'pk': LOCATION_ROOT,
            'name': 'Location',
            'name_ascii': 'Location',
            'active': True,
        })

signals.post_syncdb.connect(create_root_node, sender=models)
