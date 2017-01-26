# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from sklearn import linear_model
import dateutil.parser


def datetime2second(input_time):
    print 'isoweekday : ', input_time.isoweekday()
    print 'hour : ', input_time.hour
    print 'minutes : ', input_time.minute
    print 'seconds : ', input_time.second
    
    weekday = input_time.weekday() * 60 * 60 * 24
    hour = input_time.hour * 60 * 60
    minutes = input_time.minute * 60
    second = input_time.second
    total = weekday + hour + minutes + second

    print 'weekday to second : ', weekday
    print 'hour to second : ', hour
    print 'minutes to second : ', minutes
    print 'second to second : ', second
    print 'total : ',weekday+hour+minutes+second

    return total


def getLinearRegression(votes, now):

    list_datetime = []
    list_proportion = []
    for vote in votes:
        time = dateutil.parser.parse(vote.time)
        list_datetime.append([time])
        list_proportion.append(vote.proportion)

    regr = linear_model.LinearRegression()
    print 'list_datetime : ', list_datetime
    print 'list_proportion : ', list_proportion
    try:
        regr.fit(list_datetime, list_proportion)
        result = regr.predict([datetime2second(now)])
    except:
        print 'error' 
        result = 0


    return result

# if __name__ == '__main__':
