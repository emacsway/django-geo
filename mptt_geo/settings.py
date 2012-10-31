from django.conf import settings
from .models import Location

LOCATION_TREE_ID = getattr(
    settings,
    'GEO_LOCATION_TREE_ID',
    1
)

LOCATION_ROOT = getattr(
    settings,
    'GEO_LOCATION_ROOT',
    1
)

try:
    LOCATION_ROOT = getattr(
        settings,
        'GEO_LOCATION_ROOT',
        Location.objects.root_node(LOCATION_TREE_ID).pk or 1
    )
except Location.DoesNotExist:
    pass
