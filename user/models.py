from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets


class User(AbstractUser):
	key = models.CharField(max_length=32, default=secrets.token_hex(32))
	
	def __str__(self):
		return self.username
	
	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"

