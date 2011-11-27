from django.conf.urls.defaults import patterns, include, url
from django.views.generic import (TemplateView, ListView, DetailView,
                                CreateView, UpdateView)
from django.core.urlresolvers import reverse
from models import Coctail, Category
from views import CategoryDelete

qs_coctails = Coctail.objects.all().select_related('ingridients')
qs_categories = Category.objects.all().select_related('coctails')

urlpatterns = patterns('',
    url(r'^coctails$', ListView.as_view(queryset=qs_coctails), name='coctails'),
    url(r'^coctails/(?P<pk>\d+)$', DetailView.as_view(queryset=qs_coctails), name='coctail'),
)

urlpatterns += patterns('',
    url(r'^categories$', ListView.as_view(model=Category), name='categories'),
    url(r'^categories/add$', CreateView.as_view(model=Category), name='category_add'),
    url(r'^categories/(?P<pk>\d+)$', DetailView.as_view(queryset=qs_categories), name='category'),
    url(r'^categories/(?P<pk>\d+)/edit$', UpdateView.as_view(queryset=qs_categories), name='category_edit'),
    url(r'^categories/(?P<pk>\d+)/delete$', CategoryDelete.as_view(), name='category_delete'),
)
