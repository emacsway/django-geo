from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from mptt_geo.models import Location
from mptt_geo import forms

LOCATION_ROOT = getattr(settings, 'GEO_LOCATION_ROOT', 1)


def location_detail(request, pk=None):
    """Shows detail info for given location"""
    pk = pk or LOCATION_ROOT
    location = get_object_or_404(Location, pk=pk, active=True).get_real()
    new_location = None
    form = None

    model_class = location.get_child_class()
    if model_class and request.user.has_perm('mptt_geo.add_location', location):
        form_class = getattr(forms, '{0}Form'.format(model_class.__name__))
        form = form_class(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            new_location = form.save(commit=False)
            new_location.creator = request.user
            new_location.parent = location
            # for large trees we can save data asynchronously
            new_location.save()
            form.save_m2m()
            form = form_class(None, initial={'parent': location.pk, })
            messages.info(request,
                          _("Information has been updated successfully."))

    # New children already saved, so now get children
    children = location.get_children().filter(active=True)
    return render_to_response(
        'geo/location_detail.html',
        RequestContext(request, {
            'object': location,
            'new_object': new_location,
            'children': children,
            'form': form,
        })
    )
