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
    try:
        parm_category = request.GET['category']
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        list = RestaurantList.objects.filter(category=parm_category)
        serializer = restaurantSerializer(list, many=True)
        return JSONResponse(serializer.data)

@api_view(['GET'])
def get_all_vote(request):
    list_vote = Vote.objects.values()

    result = []
    for vote in list_vote:
        title = vote['title']
        time = vote['time']
        proportion = vote['proportion']
        sex = vote['sex']
        age = vote['age']
        result.append({'title':title, 'time':time, 'proportion':proportion, 'sex':sex, 'age':age})

    result = {'data':result}

    Vote.objects.all().delete()
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def vote_list(request):
    try:
        parm_title = request.GET['title']
        print parm_title
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        time_threshold = datetime.now() - timedelta(minutes=5)
        print 'time threshold : ',time_threshold
        list = Vote.objects.filter(created_it__gt=time_threshold, title = parm_title)# __gt means "greater than" and lookup type field.

        serializer = voteSerializer(list, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        print 'hello'
        serializer = voteSerializer(title = request.GET['title'], proportion = request.GET['proportion'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#카테고리별 가게이름을 먼저 조회한 후, 디비에 예측된 값을 조회하여 제공
@api_view(['GET'])
def current(request):
    try:
        print 1
        parm_category = request.GET['category']
        print parm_category
        parm_time = dateutil.parser.parse(request.GET['time'])
        print parm_time
        parm_time = int(parm_time.hour)*60 + int(parm_time.minute)
        print('category: ', parm_category, ' time: ', parm_time)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    list_title = list(RestaurantList.objects.filter(category=parm_category))
    response = []
    for item in list_title:
        predicted_proportion = PredictProportion.objects.filter(title = item.title, time= parm_time)

        print(len(predicted_proportion))
        if(len(predicted_proportion) == 0):
            proportion = 0
        else:
            proportion = predicted_proportion[0].proportion
        response.append({'title':item.title,'proportion':proportion})

    result = {"data":response}
    print(result)
    return Response(result, status=status.HTTP_201_CREATED)


# 투표요청시 불리는 함수 Vote객체를 만들고 저장한다.
# parameters : title, time, proportion
@api_view(['GET'])
def vote(request):
    try:
        parm_title = request.GET['title']
        parm_proportion = request.GET['proportion']
        parm_time = request.GET['time']
        parm_sex = request.GET['sex']
        parm_age = request.GET['age']
        #print ('title : ', parm_title, 'parm_proportion : ', parm_proportion, 'parm_time : ', parm_time)
        vote = Vote(title=parm_title, time=parm_time, proportion=int(parm_proportion), sex = parm_sex, age = parm_age)
        vote.save()
        return Response("Success",status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


# 가게 검색시에 호출되는 함수
# parameters : title(가게이름)
@api_view(['GET'])
def search(request):
    try:
        parm_title = request.GET['title']
        time_threshold = datetime.now() - timedelta(minutes=5)
        filter_title = RestaurantList.objects.filter(title = parm_title)
        for item in filter_title:
            print item
        if(len(filter_title)==0):
            return Response("not exist")

        filter_vote = Vote.objects.filter(created_it__gt=time_threshold, title__icontains = parm_title)

        response = []
        list_vote = []
        for vote in filter_vote:
            list_vote.append(vote.proportion)
        try:
            proportion = sum(list_vote) / len(list_vote)
        except:
            proportion = 0
        print(proportion)

        response.append({'title': parm_title, 'proportion': proportion})

        result = {"data": response}
        print(result)

        return Response(result, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)





