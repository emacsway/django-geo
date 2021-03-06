from __future__ import absolute_import, unicode_literals
import sys
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core import urlresolvers
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django_ext.db.models.polymorphic import PolymorphicModel
from django_ext.db.models.tree import MpModel

from .managers import LocationManager

if "notification" in django_settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

try:
    str = unicode  # Python 2.* compatible
except NameError:
    pass

current_module = sys.modules[__name__]

CITY_TYPES = (
    ('city', _('city')),
    ('urban_village', _('urban village')),
    ('village', _('village')),
    ('settlement', _('settlement')),
    ('farm', _('farm')),
)

CITY_ABBREVIATED_TYPES = (
    ('city', _('city')),
    ('urban_village', _('urban village')),
    ('village', _('village')),
    ('settlement', _('settlement')),
    ('farm', _('farm')),
)

CITY_ABBREVIATED_TYPES_DICT = dict(CITY_ABBREVIATED_TYPES)

STREET_TYPES = (
    ('avenue', _('avenue')),
    ('street', _('street')),
    ('passage', _('passage')),
    ('highway', _('highway')),
    ('lane', _('lane')),
    ('boulevard', _('boulevard')),
    ('square', _('square')),
    ('embankment', _('embankment')),
    ('quarter', _('quarter')),
)

STREET_ABBREVIATED_TYPES = (
    ('avenue', _('ave.')),
    ('street', _('st.')),
    ('passage', _('passage')),
    ('highway', _('highway')),
    ('lane', _('lane')),
    ('boulevard', _('boulevard')),
    ('square', _('square')),
    ('embankment', _('embankment')),
    ('quarter', _('quarter')),
)

STREET_ABBREVIATED_TYPES_DICT = dict(STREET_ABBREVIATED_TYPES)

GEONAME_NONEXISTENT = 0
GEONAME_EXISTENT = 1
GEONAME_INDEPENDENT = 2

GEONAME_STATUSES = (
    (GEONAME_NONEXISTENT, _('nonexistent'), ),
    (GEONAME_EXISTENT, _('existent'), ),
    (GEONAME_INDEPENDENT, _('independent'), ),
)

"""
Migration:
!!! First, disable modeltranslation for model !!!
# translator.register(Location, LocationTranslationOptions)
from geo.models import Location
Location.objects.get(pk=1).save()
for obj in Location.objects.exclude(pk=1).order_by('parent__pk', 'pk').iterator():
    obj.save()
"""


# TODO: Add django-versioning here
class Location(PolymorphicModel, MpModel):
    """Base location model"""
    name = models.CharField(_("official name"), max_length=255, db_index=True, null=True)
    name_ascii = models.CharField(
        _("ascii name"),
        max_length=255,
        help_text=_("latin (ascii) transliteration of name"),
        db_index=True
    )
    active = models.BooleanField(default=True, db_index=True)
    creator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_related"
    )
    child_class = models.CharField(
        _("child class"),
        max_length=80,
        blank=True,
        db_index=True
    )
    body = models.TextField(_("text"), blank=True)
    geoname_id = models.PositiveIntegerField(
        unique=True,
        blank=True,
        null=True
    )
    geoname_status = models.PositiveSmallIntegerField(
        db_index=True,
        blank=True,
        null=True,
        default=GEONAME_NONEXISTENT,
        choices=GEONAME_STATUSES
    )

    objects = LocationManager()

    class Meta:
        ordering = ['name', ]
        unique_together = (('parent', 'name', ), ('parent', 'name_ascii', ), )
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __str__(self):
        return force_text(self.name)

    def get_absolute_url(self):
        return urlresolvers.reverse('geo_location_detail', args=[self.pk])

    def get_child_class(self):
        """Returns child class"""
        if self.child_class:
            return models.get_model(*self.child_class.rsplit('.', 1))
        return models.get_model('geo', 'country')

    def is_allowed(self, user, perm=None):
        """Checks permissions."""
        base, model = perm.rsplit("_", 1)
        model = "location"
        perm = "_".join((base, model, ))

        if perm in ('geo.view_location',
                    'geo.browse_location', ):
            return True
        if perm == 'geo.add_location':
            return False
        if perm in ('geo.change_location',
                    'geo.delete_location', ):
            return False
        return False


class Country(Location):
    """Country model"""
    iso_alpha2 = models.CharField(max_length=2, unique=True)
    iso_alpha3 = models.CharField(max_length=3, unique=True)

    # objects = LocationManager()

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")

    def get_child_class(self):
        """Returns child class"""
        # for Russia can be added okrug level
        # for USSR also republic
        if self.child_class:
            return models.get_model(*self.child_class.rsplit('.', 1))
        return models.get_model('geo', 'region')


class Region(Location):
    """Region model"""

    # objects = LocationManager()

    class Meta:
        verbose_name = _("region")
        verbose_name_plural = _("regions")

    def get_child_class(self):
        """Returns child class"""
        if self.child_class:
            return models.get_model(*self.child_class.rsplit('.', 1))
        return models.get_model('geo', 'city')

    def is_allowed(self, user, perm=None):
        """Checks permissions."""
        if perm == 'geo.add_location':
            return user.is_authenticated()
        return super(Region, self).is_allowed(user, perm)


class City(Location):
    """City model"""
    city_type = models.CharField(
        verbose_name=_("Type"),
        max_length=20,
        choices=CITY_TYPES,
        default='city',
        db_index=True
    )

    # objects = LocationManager()

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")

    def __str__(self):
        return '{0} {1}'.format(
            self.get_city_type_display(),
            self.name
        )

    def get_child_class(self):
        """Returns child class"""
        if self.child_class:
            return models.get_model(*self.child_class.rsplit('.', 1))
        return models.get_model('geo', 'street')

    def is_allowed(self, user, perm=None):
        """Checks permissions."""
        if perm == 'geo.add_location':
            return user.is_authenticated()
        return super(City, self).is_allowed(user, perm)


class Street(Location):
    """Street model"""
    street_type = models.CharField(
        verbose_name=_("Type"),
        max_length=20,
        choices=STREET_TYPES,
        default='street',
        db_index=True
    )

    # objects = LocationManager()

    class Meta:
        verbose_name = _("street")
        verbose_name_plural = _("streets")

    def __str__(self):
        return '{0} {1}'.format(
            self.get_street_type_display(),
            self.name
        )

    def get_child_class(self):
        """Returns child class"""
        if self.child_class:
            return models.get_model(*self.child_class.rsplit('.', 1))
        return None

    def is_allowed(self, user, perm=None):
        """Checks permissions."""
        if perm == 'geo.add_location':
            return False
        return super(Street, self).is_allowed(user, perm)


class LocationItem(models.Model):
    location = models.ForeignKey(
        Location,
        verbose_name=_("location"),
        related_name="items"
    )
    content_type = models.ForeignKey(
        ContentType,
        related_name="geo_location_items"
    )
    object_id = models.CharField(max_length=255, db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (('location', 'content_type', 'object_id'),)
        verbose_name = _("Location item")
        verbose_name_plural = _("Location items")

    def __str__(self):
        return '{0} [{1}]'.format(self.object, self.location)


def geo_location_new(sender, instance, **kwargs):
    if isinstance(instance, Location):
        if notification:
            notify_list = User.objects.filter(
                is_active=True,
                is_superuser=True
            )
            if instance.creator:
                notify_list = notify_list.exclude(
                    id__exact=instance.creator.id
                )

            notification.send(notify_list, "geo_location_new", {
                "user": instance.creator,
                "item": instance,
                "type": instance._meta.verbose_name,
            })

models.signals.post_save.connect(geo_location_new, sender=Country)
models.signals.post_save.connect(geo_location_new, sender=Region)
models.signals.post_save.connect(geo_location_new, sender=City)
models.signals.post_save.connect(geo_location_new, sender=Street)

# Python 2.* compatible
try:
    unicode
except NameError:
    pass
else:
    for cls in (Location, City, Street, LocationItem, ):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda self: self.__unicode__().encode('utf-8')
