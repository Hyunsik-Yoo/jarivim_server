# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from lineup.models import *
from lineup.serializers import restaurantSerializer, voteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
import json
import dateutil.parser


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET'])
def restaurent_list(request):
    """
    카테고리를 입력으로 받아서 해당 카테고리에 속하는 음식점 리스트 반환
    """
    try:
        parm_category = request.GET['category']
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # 카테고리에 해당하는 음식점 오브젝트 필터링
        list = Restaurant.objects.filter(category=parm_category)
        serializer = restaurantSerializer(list, many=True)
        return JSONResponse(serializer.data)

@api_view(['GET'])
def get_all_vote(request):
    """
    하루동안의 전체 투표 가지고 오기
    JSON파일로 만들고 다음예측을 위해
    """
    list_vote = Vote.objects.values()

    serializer = voteSerializer(list_vote, many=True)
    return JSONResponse(serializer.data)


@api_view(['GET'])
def current(request):
    """
    카테고리별 가게이름을 먼저 조회한 후, 디비에 예측된 값을 조회하여 제공
    """
    try:
        parm_time = dateutil.parser.parse(request.GET['time'])
        parm_time = int(parm_time.hour)*60 + int(parm_time.minute)
        print('time: ', parm_time)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    result = {}

    list_category = list(Category.objects.all())
    for category in list_category:
        response_category = []
        list_restaurant = list(RestaurantList.objects.filter(category=category.name))
        for restaurant in list_restaurant:
            predicted_proportion = PredictProportion.objects.filter(title = restaurant.title, time= parm_time)
            if(len(predicted_proportion) == 0):
                proportion = 0
            else:
                proportion = predicted_proportion[0].proportion
            response_category.append({'title':restaurant.title,'proportion':proportion})
        result[category.name] = response_category
    return Response(result, status=status.HTTP_201_CREATED)


# 투표요청시 불리는 함수 Vote객체를 만들고 저장한다.
# parameters : title, time, proportion
@api_view(['GET'])
def vote(request):
    try:
        parm_title = request.GET['title']
        parm_proportion = request.GET['proportion']
        parm_time = request.GET['time']
        try:
            parm_sex = request.GET['sex']
        except:
            parm_sex = 'none'

        try:
            parm_age = request.GET['age']
        except:
            parm_age = 0
        vote = Vote(title=parm_title, time=parm_time, proportion = int(parm_proportion), sex = parm_sex, age = parm_age)
        vote.save()
        return Response("Success",status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)





