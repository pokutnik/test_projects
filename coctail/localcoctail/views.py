from django.core.urlresolvers import reverse
from django.views.generic import DeleteView
from models import Category, Ingridient

class CategoryDelete(DeleteView):
    queryset = Category.objects.all().select_related('coctails')
    get_success_url = lambda self: reverse('categories')

class IngridientDeleteWithCoctails(DeleteView):
    queryset = Ingridient.objects.all().select_related('coctails')
    get_success_url = lambda self: reverse('ingridients')

class IngridientDeleteFromCoctails(IngridientDeleteWithCoctails):
    def delete(self, request, *args, **kwargs):
        ingridient = self.get_object()
        for coctail in ingridient.coctails.all():
        	coctail.ingridients.remove(ingridient)

        return super(IngridientDeleteFromCoctails,self).delete(request, *args, **kwargs)
