# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django_webtest import WebTest
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


class SimpleCoctailCategory(TestCase):
    def setUp(self):
        self.c = Client()
        self.cat, new = Category.objects.get_or_create(title="Default")

    def test_coctail_list_detail(self):
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
       
    def test_category_list_detail(self):
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

class CategoryCRUD(WebTest):
    csrf_checks = False
    setup_auth = False    
    def test_add_category(self):
        self.assertEqual(Category.objects.all().count(), 0)

        url = reverse('category_add')
        res = self.app.get(url)
        self.assert_("Create" in res.content)


        form = res.form
        form['title'] = 'First category'
        res = form.submit().follow()
        self.assert_(form['title'].value in res.content)

        self.assertEqual(Category.objects.all().count(), 1)

        res = self.app.get(url)
        form['title'] = 'Second category'
        res = form.submit()
        res.follow()

        self.assertEqual(Category.objects.all().count(), 2)

    def test_add_empty_title(self):
        url = reverse('category_add')
        res = self.app.get(url)
        form = res.form
        form['title'] = ''
        res = form.submit()
        self.assert_("error" in res.content)

    def test_edit(self):
        title = "Vodka based"
        category = Category(title=title)
        category.save()
        self.assertEqual(Category.objects.all().count(), 1)

        url = category.get_absolute_url()
        res = self.app.get(url)

        edit_url = category.get_edit_url()
        self.assert_(edit_url in res.content)

        res = self.app.get(edit_url)
        self.assert_(title in res.content)
        self.assert_("Edit" in res.content)

        form = res.form
        title += ' edited'
        form['title'] = title
        datail_res = form.submit().follow()

        self.assert_(title in datail_res.content)
        self.assert_(edit_url in datail_res.content)

        self.assertEqual(Category.objects.all().count(), 1)
