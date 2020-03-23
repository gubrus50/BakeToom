from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
# For python manage.py Use makemigrations Then migrate To apply changes.


class Recipe(models.Model):
	title 		= models.CharField(max_length=100)
	author		= models.ForeignKey(User, on_delete=models.CASCADE)
	image 		= models.ImageField(default='default_recipe.jpg', upload_to='recipe_pics')
	description = models.TextField(blank=True)
	method 		= models.TextField(blank=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

	
class Category(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, db_index=True)
	title  = models.CharField(max_length=100, blank=True)
	ingredients	= models.TextField(max_length=240, db_index=True)
