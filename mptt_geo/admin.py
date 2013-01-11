from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from mptt_geo import models


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_as_node', 'parent', 'lft', 'rght',
                    'level', 'tree_id', 'active', )
    list_display_links = ('id', 'display_as_node', )
    #ordering = ('tree_id', 'lft', )
    search_fields = ('name', 'name_ascii', 'body', )
    list_filter = ('active', )
    list_editable = ('active', )
    raw_id_fields = ('creator', )

    def display_as_node(self, obj):
        return  '{0} {1}'.format(
            '>>>' * (obj.level),
            str(obj)
        )

admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Country, LocationAdmin)
admin.site.register(models.Region, LocationAdmin)
admin.site.register(models.City, LocationAdmin)
admin.site.register(models.Street, LocationAdmin)
