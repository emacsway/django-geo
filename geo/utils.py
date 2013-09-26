from django.core import urlresolvers
try:
    from tree_select.utils import add_helper
except ImportError:
    add_helper = None


def add_geo_helper(*args, **kwargs):
    """Just fabric"""
    kwargs['url'] = urlresolvers.reverse_lazy('geo_location_detail')
    return add_helper(*args, **kwargs)
