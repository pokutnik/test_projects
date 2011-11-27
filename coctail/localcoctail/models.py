# -*- coding: utf-8 -*-
from django.db import models

class Ingridient(models.Model):
	value = models.CharField("Title", max_length=140)

class Coctail(models.Model):
	title = models.CharField("Title", max_length=140)
	description = models.TextField("Description")
	category = models.ForeignKey('Category', related_name='coctails')
	ingridients = models.ManyToManyField('Ingridient', related_name='coctails')

	@models.permalink
	def get_absolute_url(self):
		return 'coctail', (self.id, )

class Category(models.Model):
	title = models.CharField("Title", max_length=140)
