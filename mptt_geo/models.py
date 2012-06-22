from django.db import models
from django.core import urlresolvers
import mptt
from mptt.models import MPTTModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

LOCATION_TYPES = [
    ('country', _('country'))
    ('region', _('region'))
    ('city', _('city'))
    ('street', _('street'))
]

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


class LocationManager(models.Manager):
    """ custom manager for locations """

    def update_locations(self, obj, locations):
        """ updates the locations for the given object """
        ctype = ContentType.objects.get_for_model(obj)
        current_location_items = LocationItem.objects.filter(content_type=ctype, object_id=obj.id)

        # delete LocationItems not present in locations
        current_location_items.exclude(location__in=locations).delete()

        # Find what locations to add
        # FIXME: is there any optimized query for this?
        locations_to_add = self.exclude(items__in=current_location_items).filter(id__in=[c.id for c in locations])

        # create categorized items  for this
        for c in locations_to_add:
            LocationItem.objects.create(location=c, object=obj)

    def get_for_model(self, model):
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(items__content_type=ctype).distinct()

    def get_for_object(self, obj):
        ctype = ContentType.objects.get_for_object(obj)
        return self.filter(items__content_type=ctype,
            object_id=obj.pk).distinct()


# TODO: Add django-versioning here
class Location(MPTTModel):
    """Base location model"""
    parent = models.ForeignKey('self', blank=True, null=True)
    type = models.CharField(_("type"), max_length=20, choices=LOCATION_TYPES)
    name = models.CharField(_("name"), max_length=255)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, blank=True, null=True,
                                on_delete=models.SET_NULL)
    text = models.TextField(_("text"), blank=True)

    #objects = LocationManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return urlresolvers.reverse('location_view', args=[self.pk])

    class Meta:
        ordering = ['tree_id', 'lft']


class Country(Location):
    """Country model"""
    iso_alpha2 = models.CharField(max_length=2, unique=True)
    iso_alpha3 = models.CharField(max_length=3, unique=True)


class City(Location):
    """City model"""
    city_type = models.CharField(
        verbose_name=_("Type"),
        max_length=20,
        choices=CITY_TYPES,
        default='city'
    )


class Street(Location):
    """Street model"""
    street_type = models.CharField(
        verbose_name=_("Type"),
        max_length=10,
        choices=STREET_TYPES
    )


class LocationItem(models.Model):
    location = models.ForeignKey(Location, verbose_name=_("location"), related_name="items")
    content_type = models.ForeignKey(ContentType, related_name="items")
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (('location', 'content_type', 'object_id'),)
        verbose_name = _("Categorized item")
        verbose_name_plural = _("Categorized items")

    def __unicode__(self):
        return u'%s [%s]' % (self.object, self.location)

try:
    mptt.register(Location)
except:
    pass
