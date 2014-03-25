from __future__ import absolute_import, unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet


class PolymorphicQuerySet(QuerySet):
    """Custom QuerySet for real instances."""

    _polymorphic = True

    def polymorphic(self, val=True):
        c = self._clone()
        c._polymorphic = val
        return c

    def iterator(self):
        for obj in super(PolymorphicQuerySet, self).iterator():
            yield obj.get_real() if self._polymorphic and hasattr(obj, 'get_real') else obj

    def _clone(self):
        c = super(PolymorphicQuerySet, self)._clone()
        c._polymorphic = self._polymorphic
        return c


class PolymorphicManager(models.Manager):
    def get_query_set(self):
        """Returns a new QuerySet object."""
        qs = super(PolymorphicManager, self).get_query_set()
        if not isinstance(qs.__class__, PolymorphicQuerySet):
            class NewPolymorphicQuerySet(PolymorphicQuerySet, qs.__class__):
                pass
            qs.__class__ = NewPolymorphicQuerySet
        return PolymorphicQuerySet(self.model, using=self._db)

    def polymorphic(self, val):
        return self.get_query_set().polymorphic(val)


class LocationManager(PolymorphicManager):
    """Custom manager for locations """
    # use_for_related_fields = True

    def update_locations(self, obj, locations):
        """ updates the locations for the given object """
        from .models import LocationItem
        ctype = ContentType.objects.get_for_model(obj)
        current_location_items = LocationItem.objects.filter(
            content_type=ctype,
            object_id=obj.id
        )

        # delete LocationItems not present in locations
        current_location_items.exclude(location__in=locations).delete()

        # Find what locations to add
        # FIXME: is there any optimized query for this?
        locations_to_add = self.exclude(
            items__in=current_location_items
        ).filter(
            id__in=[c.id for c in locations]
        )

        # create categorized items  for this
        for c in locations_to_add:
            LocationItem.objects.create(location=c, object=obj)

    def get_for_model(self, model):
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(items__content_type=ctype).distinct()

    def get_for_object(self, obj):
        ctype = ContentType.objects.get_for_object(obj)
        return self.filter(items__content_type=ctype, object_id=obj.pk).distinct()
