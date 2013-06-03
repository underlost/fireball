from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.RecentView.as_view(), name='home'),
	url(r'^screenshot/(?P<blob_id>\d*)/$', views.SingleBlob, name='single'),
	url(r'^screenshot/full/(?P<blob_id>\d*)/$', views.FullSizeBlob, name='fullsize'),
	url(r'^(?P<username>[\w-]+)/$', views.UserView.as_view(), name='user'),
	
    url(r'^infinite/$', views.infinite, name='infinite'),
    url(r'^submit/$', views.new_blob, name='new-blob'),    
    
    #Delete
    url(r'^delete/(?P<blob_id>\d*)/$', views.delete_blob, name='delete-blob'),
    
    #Edit
    #url(r'^edit/(?P<blob_id>\d+)/$', views.edit_entry, name = 'edit-blob'),
    
    
)
