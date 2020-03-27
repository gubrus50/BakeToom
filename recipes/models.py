from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from PIL import Image


# Create your models here.
# For python manage.py Use makemigrations Then migrate To apply changes.


class Recipe(models.Model):
	title 		= models.CharField(max_length=100, verbose_name= _('Tytuł przepisu'))
	author		= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name= _('Autor'))
	image 		= models.ImageField(default='default_recipe.jpg', upload_to='recipe_pics', verbose_name= _('Wprowadź Obraz'))
	description = models.TextField(blank=True, verbose_name= _('Krutka deskrypcja przepisu'))
	method 		= models.TextField(blank=True, verbose_name= _('Wprowadź instrukcję sukcesywnego wykonania produktu'))

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
	title = models.CharField(max_length=100, blank=True, verbose_name= _('Tytuł kategorii'))
	ingredients	= models.TextField(max_length=240, db_index=True, verbose_name= _('Wprowadź listę składników do następującej kategorii'))
