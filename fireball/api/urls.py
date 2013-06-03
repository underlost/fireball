from django.conf.urls import patterns, include, url

from .api import BlobResource
from .api import UserResource


blob_resource = BlobResource()
user_resource = UserResource()


urlpatterns = patterns('',
    url(r'', include(blob_resource.urls)),
    url(r'', include(user_resource.urls)),
    url(r'^blobs/recent/(?P<page>\d*)/$', 'fireball.api.views.blobs_recent', name='blobs-recent'),
)
