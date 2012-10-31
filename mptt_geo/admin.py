from django.contrib import admin
from mptt_geo import models


class LocationAdmin(admin.ModelAdmin):
    list_display = ('display_as_node', 'lft', 'rght', 'level', 'tree_id', 'active', )
    #ordering = ('tree_id', 'lft', )
    search_fields = ('name', 'name_ascii', 'body', )
    list_filter = ('active', )
    list_editable = ('active', )

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
