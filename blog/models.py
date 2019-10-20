# blog/models.py
from django.db import models
from garden.models import Garden
import datetime
from django.utils.dateparse import parse_date

def upload_to(instance, filename):
    return 'users/%s/%s' % (instance.garden.serial, filename)

class Picture(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    date = models.DateField()
    photo = models.ImageField(upload_to=upload_to)
    temp_high = models.IntegerField(default=0)
    temp_low = models.IntegerField(default=0)
    humidity_high = models.IntegerField(default=0)
    humidity_low = models.IntegerField(default=0)
    comments = models.TextField()
    
    class Meta:
        ordering=['-date']
# Create your models here.
