from __future__ import absolute_import, unicode_literals
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('geo.views',
    url(r'(?:(?P<pk>[0-9]+)/)?$', 'location_detail',
        name='geo_location_detail'),
)
