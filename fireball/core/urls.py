from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^private/$', 'fireball.core.views.private', name='private'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}, name='login'),
    url(r'^register/$', 'fireball.core.views.register', name='register'),
    url(r'^logout/$', 'fireball.core.views.logout_user', name='logout'),

	#Static
	url(r'^about/$', TemplateView.as_view(template_name="static/about.html")),
	url(r'^about/api/$', TemplateView.as_view(template_name="static/api.html")),
	url(r'^about/terms/$', TemplateView.as_view(template_name="static/terms.html")),
	url(r'^about/privacy/$', TemplateView.as_view(template_name="static/privacy.html")),

)
