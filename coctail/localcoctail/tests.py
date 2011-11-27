# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

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


class CoctailsCrud(TestCase):
    def setUp(self):
        self.c = Client()
        self.cat, new = Category.objects.get_or_create(title="Default")

    def test_list_detail(self):
        url = reverse('coctails')
        res = self.c.get(url)
        self.assertContains(res, "Coctails list")

        title = "EmptyCoctail"
        self.assertNotContains(res, title)

        coctail = Coctail(title=title, category=self.cat)
        coctail.save()
        res = self.c.get(url)
        self.assertContains(res, title)

        url = coctail.get_absolute_url()
        self.assertContains(res, url)

        res = self.c.get(url)
        self.assertContains(res, title)
        

class CategoryCRUD(TestCase):
    def setUp(self):
        self.c = Client()
    
    def test_list(self):
        url = reverse('categories')
        res = self.c.get(url)
        self.assertContains(res, "Categories list")

        title = "Vodka based"
        self.assertNotContains(res, title)

        category = Category(title=title)
        category.save()
        res = self.c.get(url)
        self.assertContains(res, title)

        url = category.get_absolute_url()
        self.assertContains(res, url)

        res = self.c.get(url)
        self.assertContains(res, title)

        coctail_title = "Stopka"
        coctail = Coctail(title=coctail_title, category=category)
        coctail.save()
        res = self.c.get(url)
        self.assertContains(res, title)

