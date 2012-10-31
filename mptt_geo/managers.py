from __future__ import absolute_import, unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet
from mptt.managers import TreeManager


class RealQuerySet(QuerySet):
    """Custom QuerySet for real instances."""

    def __getitem__(self, k):
        result = super(RealQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.get_real()
        else:
            return result

    def __iter__(self):
        for item in super(RealQuerySet, self).__iter__():
            yield item.get_real()


class LocationManager(TreeManager):
    """Custom manager for locations """

    def get_query_set(self):
        """Returns a new QuerySet object."""
        return RealQuerySet(self.model, using=self._db)

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
        return self.filter(items__content_type=ctype,
            object_id=obj.pk).distinct()
