from django.db.models import signals, get_app
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_noop as _

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
