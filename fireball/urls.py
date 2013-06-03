from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
    url(r'', include('fireball.core.urls', namespace='core')),
    url(r'', include('fireball.blobs.urls', namespace='blobs')),
    url(r'^api/', include('fireball.api.urls', namespace='api')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
