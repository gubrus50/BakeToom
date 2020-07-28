from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = ResizedImageField(
		size=[300, 300],
		crop=['middle', 'center'],
		quality=75,
		force_format='JPEG',
		upload_to='profile_pics',
		default='default_profile.jpg'
	)

	def __str__(self):
		return f'{self.user.username} Profile'