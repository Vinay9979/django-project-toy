from django.db import models
from client.models import Category

# Create your models here.
class Categoryphotos(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    imgUrl = models.URLField()

    class Meta:
        db_table = 'categoryphotos'
