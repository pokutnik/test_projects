from django.core.urlresolvers import reverse
from django.views.generic import DeleteView
from models import Category

class CategoryDelete(DeleteView):
    queryset = Category.objects.all().select_related('coctails')
    get_success_url = lambda self: reverse('categories')
