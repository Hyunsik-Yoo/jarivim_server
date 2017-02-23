from __future__ import unicode_literals

from django.db import models
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Vote(models.Model):
    created_it = models.TimeField(blank=False, auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, default='')
    time = models.CharField(max_length=100, blank=False, default='')
    proportion = models.IntegerField(blank=False, default=0)
    sex = models.CharField(max_length=6, blank=False, default='')
    age = models.IntegerField(blank=False, default=0)

    def __str__(self):
        result = str(self.title) + '(' + str(self.proportion) + ')'
        return result

class RestaurantList(models.Model):
    category = models.CharField(max_length=100, blank=False, default='bob')
    title = models.CharField(max_length=100, blank=False, default='')

    def __str__(self):
        result = str(self.title) + '(' + str(self.category) + ')'
        return result

class PredictProportion(models.Model):
    time = models.CharField(max_length=100, blank=False, default='')
    title = models.CharField(max_length=100, blank=False, default='')
    proportion = models.IntegerField(blank=False, default=0)

class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, default='bob')

    def __str__(self):
        return self.name


# Create your models here.
