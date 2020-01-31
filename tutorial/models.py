from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ques(models.Model):
	question = models.CharField(max_length=200)
	answer = models.TextField()
	likes = models.IntegerField(default=0)
	date_asked = models.DateTimeField(default=timezone.now)
	asked_by = models.CharField(max_length=50)
	
	def __str__(self):
		return self.question	 