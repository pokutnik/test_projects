"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from models import Category, Ingridient, Coctail

class ModelsTest(TestCase):
    def test_simple_models(self):
    	coctail = Coctail(title="Margarita")
    	category = Category(title="Alcohol based")
    	category.save()
    	coctail.category = category
    	coctail.save()

    	vodka = Ingridient(value='Vodka 50g')
    	vodka.save()
    	coctail.ingridients.add(vodka)
    	coctail.save()

    	self.assertEqual(Coctail.objects.all().count(), 1)
    	self.assertEqual(Category.objects.all().count(), 1)
    	self.assertEqual(Ingridient.objects.all().count(), 1)
    	self.assertEqual(category.coctails.all().count(), 1)
        self.assertEqual(vodka.coctails.all().count(), 1)