from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import io
from django.core.files.storage import default_storage as storage



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'