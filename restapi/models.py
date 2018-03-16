from django.db import models
from django.utils import timezone
import os
from .functions import random_filename


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    screenshot = models.CharField(max_length=100,blank=True)
    name = models.CharField(max_length=100)
    type_of_feedback = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        	return self.name + " " + str(self.timestamp)
