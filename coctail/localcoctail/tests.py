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

    def test_delete(self):
        title = "Vodka based"
        category = Category(title=title)
        category.save()
        self.assertEqual(Category.objects.all().count(), 1)

        url = category.get_absolute_url()
        res = self.app.get(url)

        del_url = category.get_delete_url()
        res = self.app.get(del_url)
        form = res.forms["delete_form"]
        res = form.submit().follow()
        self.assertEqual(Category.objects.all().count(), 0)

    def test_delete_with_coctails(self):
        title = "Vodka based"
        category = Category(title=title)
        category.save()

        Coctail(title="Pure vodka", category=category).save()
        Coctail(title="Only vodka", category=category).save()

        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(Coctail.objects.all().count(), 2)

        del_url = category.get_delete_url()
        res = self.app.get(del_url)
        form = res.forms["delete_form"]
        res = form.submit().follow()
        
        self.assertEqual(Category.objects.all().count(), 0)
        self.assertEqual(Coctail.objects.all().count(), 0)


class IngridientCRU(WebTest):
    csrf_checks = False
    setup_auth = False

    def test_ingridient_add(self):
        self.assertEqual(Ingridient.objects.all().count(), 0)
        
        url = reverse('ingridient_add')
        res = self.app.get(url)

        form = res.form
        form['value'] = 'Vodka 50g'
        res = form.submit().follow()

        self.assert_(form['value'].value in res.content)
        self.assertEqual(Ingridient.objects.all().count(), 1)

    def test_ingridient_list_detail(self):
        ingridient = Ingridient(value='Vodka 50g')
        ingridient.save()

        list_res = self.app.get(reverse('ingridients'))
        url = ingridient.get_absolute_url()
        self.assert_(url in list_res.content)

        detail_res = self.app.get(url)
        self.assert_(ingridient.value in detail_res.content)
    
    def test_ingridient_edit(self):
        ingridient = Ingridient(value='Vodka 50g')
        ingridient.save()
        self.assertEqual(Ingridient.objects.all().count(), 1)
        
        edit_url = ingridient.get_edit_url()
        res = self.app.get(edit_url)
        form = res.form
        self.assertEqual(form['value'].value, ingridient.value)
        form['value'] = 'Vodka 100g'
        res = form.submit().follow()
        self.assert_(form['value'].value in res.content)
        self.assertEqual(Ingridient.objects.all().count(), 1)

class IngridientsDelete(WebTest):
    csrf_checks = False
    setup_auth = False
    def setUp(self):
        title = "Vodka based"
        category = Category(title=title)
        category.save()
        coctail = Coctail(title="Pure vodka", category=category)
        coctail.save()
        vodka = Ingridient(value="Vodka 100g")
        vodka.save()
        coctail.ingridients.add(vodka)
        coctail.save()

        self.vodka = vodka

        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(Ingridient.objects.all().count(), 1)
        self.assertEqual(Coctail.objects.all().count(), 1)

    def test_ingridient_delete_with_coctails(self):
        del_url = self.vodka.get_delete_url()
        res = self.app.get(del_url)
        form = res.forms["delete_with_coctails"]
        res = form.submit().follow()
        
        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(Ingridient.objects.all().count(), 0)
        self.assertEqual(Coctail.objects.all().count(), 0)

    def test_ingridient_delete_with_coctails(self):
        del_url = self.vodka.get_delete_url()
        res = self.app.get(del_url)
        form = res.forms["delete_from_coctails"]
        res = form.submit().follow()
        
        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(Ingridient.objects.all().count(), 0)
        self.assertEqual(Coctail.objects.all().count(), 1)
