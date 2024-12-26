from django.db import models

# Create your models here.
class Meeting(models.Model):
    name = models.CharField(max_length=250)
    code_name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    time = models.TimeField(auto_now=True, editable=True)