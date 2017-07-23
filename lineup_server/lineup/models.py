from __future__ import unicode_literals

from django.db import models
import datetime
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

class Vote(models.Model):
    """
    사용자 투표 형태
    (가게이름, 시간, 인구비율, 성별, 나이)
    가게이름, 시간, 인구비율만 존재하면 되지만, 분석을 위해 성별, 나이도 같이 받음)
    """
    created_it = models.TimeField(blank=False, auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, default='')
    time = models.CharField(max_length=100, blank=False, default='')
    proportion = models.IntegerField(blank=False, default=0)

    def __str__(self):
        # admin페이지에서 한눈에 알아보려고 Override함
        result = str(self.title) + '(' + str(self.proportion) + ')'
        return result

class Restaurant(models.Model):
    """
    가게리스트 (카테고리, 가게이름)
    """
    category = models.CharField(max_length=100, blank=False, default='bob')
    title = models.CharField(max_length=100, blank=False, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    latitude = models.CharField(max_length=20, blank=False, default='')
    longitude = models.CharField(max_length=20, blank=False, default='')
    menu = models.CharField(max_length=3000, blank=True, default='')

    def __str__(self):
        result = str(self.title) + '(' + str(self.category) + ')'
        return result

class PredictProportion(models.Model):
    """
    예측한 결과
    (시간, 가게이름, 인구비율)
    """
    time = models.CharField(max_length=100, blank=False, default='')
    title = models.CharField(max_length=100, blank=False, default='')
    proportion = models.IntegerField(blank=False, default=0)

class Category(models.Model):
    """
    가게 카테고리 (카테고리 이름)
    """
    name = models.CharField(max_length=100, blank=False, default='bob')

    def __str__(self):
        return self.name


