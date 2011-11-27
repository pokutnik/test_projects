# -*- coding: utf-8 -*-
from django.db import models

class Ingridient(models.Model):
	value = models.CharField("Title", max_length=140)
	@models.permalink
	def get_absolute_url(self):
		return 'ingridient', (self.id, )

	@models.permalink
	def get_edit_url(self):
		return 'ingridient_edit', (self.id, )

	@models.permalink
	def get_delete_url(self):
		return 'ingridient_delete_with_coctails', (self.id, )


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
	@models.permalink
	def get_absolute_url(self):
		return 'category', (self.id, )

	@models.permalink
	def get_edit_url(self):
		return 'category_edit', (self.id, )

	@models.permalink
	def get_delete_url(self):
		return 'category_delete', (self.id, )


	
