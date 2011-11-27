from django.conf.urls.defaults import patterns, include, url

from django.views.generic import TemplateView, ListView, DetailView
from models import Coctail, Category

qs_coctails = Coctail.objects.all().select_related('ingridients')
qs_categories = Category.objects.all().select_related('coctails')

urlpatterns = patterns('',
    url(r'^coctails$', ListView.as_view(queryset=qs_coctails), name='coctails'),
    url(r'^coctails/(?P<pk>\d+)$', DetailView.as_view(queryset=qs_coctails), name='coctail'),

    url(r'^categories$', ListView.as_view(model=Category), name='categories'),
    url(r'^categories/(?P<pk>\d+)$', DetailView.as_view(queryset=qs_categories), name='category'),
)
