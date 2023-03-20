from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django_resized import ResizedImageField


class Recipe(models.Model):

	RECIPE_TYPE_CHOICES = (
		('pastry', 'pastry'),
		('dessert', 'dessert'),
		('soup', 'soup'),
		('other', 'other')
	)

	DEFAULT_LICENSE = (
		'MIT License'
		'\n\n'
		'Copyright (c) [year] [fullname]'
		'\n\n'
		'Permission is hereby granted, free of charge, to any person obtaining a copy '
		'of this software and associated documentation files (the "Software"), to deal '
		'in the Software without restriction, including without limitation the rights '
		'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell '
		'copies of the Software, and to permit persons to whom the Software is '
		'furnished to do so, subject to the following conditions:'
		'\n\n'
		'The above copyright notice and this permission notice shall be included in all '
		'copies or substantial portions of the Software.'
		'\n\n'
		'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR '
		'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, '
		'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE '
		'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER '
		'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, '
		'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE '
		'SOFTWARE.'
	)

	title = models.CharField(
		max_length=100,
		verbose_name=_('Recipe name')
	)

	publisher = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		verbose_name=_('Publisher')
	)

	recipe_type	= models.CharField(
		max_length=100,
		blank=False,
		default=RECIPE_TYPE_CHOICES[3][1],
		choices=RECIPE_TYPE_CHOICES,
		verbose_name=_('Recipe type')
	)

	certified = models.BooleanField(
		blank=False,
		default=False
	)

	published = models.BooleanField(
		blank=False,
		default=False,
		verbose_name=_('I agree with the conditions presented to me and publish my recipe')
	)

	image = ResizedImageField(
		size=[300, 300],
		crop=['middle', 'center'],
		quality=75,
		force_format='JPEG',
		upload_to='recipe_pics',
		default='default_recipe.jpg',
		verbose_name=_('Enter image')
	)

	description = models.TextField(
		max_length=400,
		blank=True,
		verbose_name=_('A brief description of the recipe')
	)

	method = models.TextField(
		max_length=10000,
		blank=True,
		verbose_name=_('Recipe guide/instructions')
	)

	license	= models.TextField(
		max_length=10000,
		blank=False,
		default=DEFAULT_LICENSE,
		verbose_name=_('Create licence')
	)

	nationality	= CountryField(
		max_length=100,
		blank=True,
		blank_label='International',
		verbose_name=_('Select recipe\'s nationality')
	)

	date_posted_old = models.DateTimeField(blank=True, null=True)
	date_posted		= models.DateTimeField(blank=True, null=True)
	date_created	= models.DateTimeField(blank=False, default=timezone.now)
	date_edited		= models.DateTimeField(blank=True, null=True)


	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):


		if not self.date_edited:
			self.date_edited = self.date_created
		else:
			self.date_edited = timezone.now()

		if self.published:
			if self.date_posted == self.date_created:
				self.date_posted = timezone.now()

			elif not self.date_posted_old:
				self.date_posted_old = timezone.now()
		else:
			if not self.date_posted and self.date_posted_old:
				self.date_posted = self.date_posted_old

			if self.date_posted_old and self.date_posted == self.date_posted_old:
				self.date_posted = self.date_created

			elif self.date_posted:
				self.date_posted = self.date_created

		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('recipe-detail', kwargs={'pk': self.pk})

	


class Category(models.Model):

	recipe = models.ForeignKey(
		Recipe,
		on_delete=models.CASCADE,
		db_index=True
	)

	name = models.CharField(
		max_length=100,
		blank=True,
		verbose_name= _('Categorie\'s title')
	)

	ingredients	= models.TextField(
		max_length=500,
		db_index=True,
		verbose_name= _('Enter the list of ingredients into the following category')
	)

	class Meta:
		verbose_name_plural = 'Categories'