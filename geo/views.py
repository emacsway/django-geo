from __future__ import absolute_import, unicode_literals
from django.contrib import messages
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _

from .models import Location
from . import forms, settings


def location_detail(request, pk=None):
    """Shows detail info for given location"""
    pk = request.POST.get('parent') or pk or settings.LOCATION_ROOT
    location = get_object_or_404(Location, pk=pk, active=True).get_real()
    new_location = None
    form = None
    model_class = location.get_child_class()
    if model_class and request.user.has_perm('geo.add_location',
                                             location):
        initial = {'parent': location, }
        form_class = getattr(forms, '{0}Form'.format(model_class.__name__))
        form = form_class(request.POST or None, initial=initial)
        if request.method == 'POST' and form.is_valid():
            new_location = form.save(commit=False)
            new_location.creator = request.user
            # for large trees we can save data asynchronously
            new_location.save()
            form.save_m2m()
            form = form_class(None, initial=initial)
            messages.info(request,
                          _("Information has been saved successfully."))
            return redirect(new_location.get_absolute_url())

    # New children already saved, so now get children
    children = location.get_children().filter(active=True)
    return render_to_response(
        'geo/location_detail.html',
        RequestContext(request, {
            'object': location,
            'opts': location._meta,
            'child_opts': model_class and model_class._meta,
            'new_object': new_location,
            'children': children,
            'form': form,
        })
    )
