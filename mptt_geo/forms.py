from django import forms
from django.db import transaction
from django.db.models import Q
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

from mptt.forms import *

from mptt_categories.models import Category

"""
class CategoryChoiceField(forms.ModelChoiceField):

    def __init__(self, level_indicator=u'---', *args, **kwargs):
        self.level_indicator = level_indicator
        if 'queryset' in kwargs.keys():
            if kwargs['queryset'].model != Category:
                raise TypeError, "This field only accepts querysets of Categories"
        else:
            kwargs['queryset'] = Category.objects.all()
        super(CategoryChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return u'%s %s' % (self.level_indicator * obj.level,
            smart_unicode(obj))

class CategoryMultipleChoiceField(forms.MultipleChoiceField):
    def __init__(self, level_indicator=u'---', *args, **kwargs):
        self.level_indicator = level_indicator
        if 'queryset' in kwargs.keys():
            if kwargs['queryset'].model != Category:
                raise TypeError, "This field only accepts querysets of categories"
        else:
            kwargs['queryset'] = Category.objects.all()
        super(CategoryMultipleChoiceField, self).__init__(*args, **kwargs)
    # the method is the same so use the same method
    label_from_instance = CategoryChoiceField.label_from_instance
"""

class CategoryModelForm2(MoveNodeForm):
    class Meta:
        model = Category

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        #fields = ['name', 'parent']

    parent = TreeNodeChoiceField(empty_label=_("Root Node"), required=False, queryset = Category.objects.all())

