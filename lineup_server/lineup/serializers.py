# -*- coding: utf-8 -*-
from rest_framework import serializers
from lineup.models import *


class restaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('category', 'title', 'phone_number', 'latitude', 'longitude', 'menu')

class voteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('title', 'time', 'proportion')

class predictSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictProportion
        fields = ('time', 'title', 'proportion')

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name')
