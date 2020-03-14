from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Recipe(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	#image = models.CharField(max_length=100) 
	title = models.CharField(max_length=100)
	description = models.TextField()
	#method = models.TextField()

	def __str__(self):
		return self.title