from django.db import models

# Create your models here.

from django.db import models

class tuple(models.Model):
    title=models.CharField(max_length=30,default="123")
    arrivalRate=models.FloatField()
    arrivalCV=models.FloatField()
    serviceRate=models.FloatField()
    serviceTimeCV=models.FloatField()
    speed=models.FloatField()
    predicted=models.IntegerField()
    def __str__(self):
        return self.title