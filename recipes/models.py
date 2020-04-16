from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from PIL import Image


# Create your models here.
# For python manage.py Use makemigrations Then migrate To apply changes.


class Recipe(models.Model):

	default_license = (
		'MIT License'
		'\n\n'
		'Copyright (c) [rok] [pełne imię i nazwisko]'
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

	title 		= models.CharField(max_length=100, verbose_name= _('Tytuł przepisu'))
	author		= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name= _('Autor'))
	image 		= models.ImageField(default='default_recipe.jpg', upload_to='recipe_pics', verbose_name= _('Wprowadź Obraz'))
	description = models.TextField(max_length=400, blank=True, verbose_name= _('Krutka deskrypcja przepisu'))
	method 		= models.TextField(max_length=10000, blank=True, verbose_name= _('Wprowadź instrukcję sukcesywnego wykonania produktu'))
	license		= models.TextField(max_length=10000, blank=False, default=default_license, verbose_name= _('Utwórz wiarygodną licencję'))

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

	def get_absolute_url(self):
		return reverse('recipe-detail', kwargs={'pk': self.pk})

	
class Category(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, db_index=True)
	name = models.CharField(max_length=100, blank=True, verbose_name= _('Tytuł kategorii'))
	ingredients	= models.TextField(max_length=500, db_index=True, verbose_name= _('Wprowadź listę składników do następującej kategorii'))

	class Meta:
		verbose_name_plural = 'Categories'