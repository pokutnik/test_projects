from django.conf.urls.defaults import patterns, include, url
from django.views.generic import (TemplateView, ListView, DetailView,
                                CreateView, UpdateView)
from django.core.urlresolvers import reverse
from models import Coctail, Category, Ingridient
from views import (CategoryDelete, IngridientDeleteWithCoctails,
                IngridientDeleteFromCoctails)

qs_coctails = Coctail.objects.all().select_related('ingridients')
qs_categories = Category.objects.all().select_related('coctails')
qs_ingridients = Ingridient.objects.all()

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

urlpatterns += patterns('',
    url(r'^ingridients$', ListView.as_view(model=Ingridient), name='ingridients'),
    url(r'^ingridients/add$', CreateView.as_view(model=Ingridient), name='ingridient_add'),
    url(r'^ingridients/(?P<pk>\d+)$', DetailView.as_view(queryset=qs_ingridients), name='ingridient'),
    url(r'^ingridients/(?P<pk>\d+)/edit$', UpdateView.as_view(queryset=qs_ingridients), name='ingridient_edit'),
    url(r'^ingridients/(?P<pk>\d+)/delete$', IngridientDeleteWithCoctails.as_view(), name='ingridient_delete_with_coctails'),
    url(r'^ingridients/(?P<pk>\d+)/delete_from_coctails$', IngridientDeleteFromCoctails.as_view(), name='ingridient_delete_from_coctails'),
)
