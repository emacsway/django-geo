from django.contrib import admin
from mptt_categories.models import Category
from mptt_categories.forms import CategoryModelForm

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryModelForm
    list_display = ('display_as_node', 'lft', 'rght', 'level', 'tree_id')
    #list_filter = ('translation__name',)
    #ordering = ('tree_id', 'lft',)
    
    def display_as_node(self, obj):
        return  u'%s %s' % (
            u'>>>' * (obj.level),
            unicode(obj)
        )

admin.site.register(Category, CategoryAdmin)
