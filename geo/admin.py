from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from . import models


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'parent', 'active', )
    list_display_links = ('id', 'name', )
    search_fields = ('name', 'name_ascii', 'body', )
    list_filter = ('active', 'content_type', )
    list_editable = ('active', )
    raw_id_fields = ('creator', )


admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Country, LocationAdmin)
admin.site.register(models.Region, LocationAdmin)
admin.site.register(models.City, LocationAdmin)
admin.site.register(models.Street, LocationAdmin)
