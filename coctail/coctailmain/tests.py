"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client


class IndexView(TestCase):
    def test_404(self):
        c = Client()
        res = c.get('/non-existing-page')
        self.assertContains(res, "Sorry", status_code=404)
                
    def test_index(self):
        c = Client()
        res = c.get('/')
        self.assertContains(res, "Welcome to Coctails site")