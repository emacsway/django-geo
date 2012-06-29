import sys
from django.db import models
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
import mptt
from mptt.models import MPTTModel
from mptt.managers import TreeManager

try:
    from tree_select.db_fields import TreeForeignKey
except ImportError:
    from mptt.fields import TreeForeignKey

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


class LocationManager(TreeManager):
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
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    parent = models.TreeForeignKey(
        'Location',
        verbose_name=_("Parent node"),
        blank=True,
        null=True  # null for top level
    )
    name = models.CharField(_("Official name"), max_length=255, db_index=True)
    name_ascii = models.CharField(
        _("ascii name"),
        max_length=255,
        help_text=_("Latin (ascii) transliteration of name"),
        db_index=True
    )
    active = models.BooleanField(default=True, db_index=True)
    creator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    body = models.TextField(_("text"), blank=True)

    #objects = LocationManager()

    class Meta:
        ordering = ['tree_id', 'lft']
        unique_together = (('parent', 'name', ), ('parent', 'name_ascii', ), )
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Sets content_type and calls parent method."""
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        return super(Location, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return urlresolvers.reverse('location_view', args=[self.pk])

    def get_real(self):  # or get_downcast(self)
        """returns instance of real class"""
        model = self.content_type.model_class()
        if model == self.__class__:
            return self
        return model.objects.get(pk=self.pk) 
        """
        for attr_name in dir(self):
            if attr_name == 'parent':
                continue
            attr = getattr(self, attr_name)
            if isinstance(attr, Location):
                return attr
        """
        return self

    def get_child_class(self):
        """Returns child class"""
        return models.get_model('mptt_geo', 'country')

    def get_children(self):
        """Fix for MTI"""
        if self.__class__ != Location:  # It's a sub-model
            return Location.get_children(self)
        else:
            return super(Location, self).get_children()

    def is_allowed(self, perm, user=None):
        """Checks permissions."""
        if perm in ('mptt_geo.view_location',
                    'mptt_geo.browse_location', ):
            return True
        if perm == 'mptt_geo.add_location':
            return False
        if perm in ('mptt_geo.change_location',
                    'mptt_geo.delete_location', ):
            return False
        return False


class Country(Location):
    """Country model"""
    iso_alpha2 = models.CharField(max_length=2, unique=True)
    iso_alpha3 = models.CharField(max_length=3, unique=True)

    class Meta:
        verbose_name = _("counntry")
        verbose_name_plural = _("countries")

    def get_child_class(self):
        """Returns child class"""
        # for Russia can be added okrug level
        # for USSR also republic
        return models.get_model('mptt_geo', 'region')


class Region(Location):
    """Region model"""

    class Meta:
        verbose_name = _("region")
        verbose_name_plural = _("regions")

    def get_child_class(self):
        """Returns child class"""
        return models.get_model('mptt_geo', 'city')

    def is_allowed(self, perm, user=None):
        """Checks permissions."""
        if perm == 'mptt_geo.add_location':
            return True
        return parent(Region, self).is_allowed(perm, user)


class City(Location):
    """City model"""
    city_type = models.CharField(
        verbose_name=_("Type"),
        max_length=20,
        choices=CITY_TYPES,
        default='city',
        db_index=True
    )

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")

    def get_child_class(self):
        """Returns child class"""
        return models.get_model('mptt_geo', 'street')

    def is_allowed(self, perm, user=None):
        """Checks permissions."""
        if perm == 'mptt_geo.add_location':
            return True
        return parent(City, self).is_allowed(perm, user)


class Street(Location):
    """Street model"""
    street_type = models.CharField(
        verbose_name=_("Type"),
        max_length=20,
        choices=STREET_TYPES,
        default='street',
        db_index=True
    )

    class Meta:
        verbose_name = _("street")
        verbose_name_plural = _("streets")

    def get_child_class(self):
        """Returns child class"""
        return None

    def is_allowed(self, perm, user=None):
        """Checks permissions."""
        if perm == 'mptt_geo.add_location':
            return False
        return parent(Street, self).is_allowed(perm, user)


class LocationItem(models.Model):
    location = models.ForeignKey(Location, verbose_name=_("location"), related_name="items")
    content_type = models.ForeignKey(ContentType, related_name="items")
    object_id = models.CharField(max_length=255, db_index=True)
    object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (('location', 'content_type', 'object_id'),)
        verbose_name = _("Location item")
        verbose_name_plural = _("Location items")

    def __unicode__(self):
        return u'%s [%s]' % (self.object, self.location)


def geo_location_new(sender, instance, **kwargs):
    if isinstance(instance, Location):
        if notification:
            notify_list = User.objects.filter(is_active=True, is_superuser=True).all() #.exclude(id__exact=instance.user.id)

            notification.send(notify_list, "geo_location_new", {
                "user": instance.creator, 
                "item": instance,
                "type": instance.get_type_display(),
            })

models.signals.post_save.connect(geo_location_new, sender=Location)
