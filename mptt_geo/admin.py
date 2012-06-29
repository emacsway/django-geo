from django.contrib import admin
from mptt_geo import models


class LocationAdmin(admin.ModelAdmin):
    list_display = ('display_as_node', 'lft', 'rght', 'level', 'tree_id', )
    #ordering = ('tree_id', 'lft', )

    def display_as_node(self, obj):
        return  u'%s %s' % (
            u'>>>' * (obj.level),
            unicode(obj)
        )

admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Country, LocationAdmin)
admin.site.register(models.Region, LocationAdmin)
admin.site.register(models.City, LocationAdmin)
admin.site.register(models.Street, LocationAdmin)
