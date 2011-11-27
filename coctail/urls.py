from django.conf.urls.defaults import patterns, include, url

from django.views.generic import TemplateView

urlpatterns = patterns('',
    (r'^$', TemplateView.as_view(template_name="index.html")),
    (r'^local/', include('localcoctail.urls')),
)
