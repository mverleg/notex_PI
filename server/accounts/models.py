
import string
from random import choice
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class IndexUser(AbstractUser):

	key = models.CharField(max_length=32, validators=[
		MinLengthValidator(32),
	])

	ALLOWED = string.printable.rstrip()

	def save(self, *args, **kwargs):
		if not self.key:
			self.generate_new_key()
		super(IndexUser, self).save(*args, **kwargs)

	def generate_new_key(self):
		self.key = ''.join(choice(self.ALLOWED) for k in range(32))
		return self.key


