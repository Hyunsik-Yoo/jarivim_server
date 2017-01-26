from sklearn import linear_model
import urllib2
import json
import dateutil.parser
import sqlite3
import time

#전체 투표 가지고오고 db에서 삭제
vote_list = urllib2.urlopen("http://192.168.2.102:8000/lineup/getvote/").read()
json_data = json.loads(vote_list)

vote_list = json_data['data']

vote_dict = dict()

# 전체 투표를 dictionary형태로 변환
for item in vote_list:
    title = item['title']
    proportion = item['proportion']
    minute = dateutil.parser.parse(item['time'])
    minute =  int(minute.hour)*60 + int(minute.minute) # 시간은 분단위로 계산
    
    # 동일키가 존재하면 append, 없으면 새로운 dictionary 생성
    if title in vote_dict.keys():
        vote_dict[title]['time'].append([minute])
        vote_dict[title]['proportion'].append(proportion)
    else:
        kv = dict()
        kv['time'] = [[minute]]
        kv['proportion'] = [proportion]
        vote_dict[title] = kv

regr = linear_model.LinearRegression()

db_connector = sqlite3.connect('db.sqlite3')
db_cursor = db_connector.cursor()

for title in vote_dict.keys():
    print title
    x_axis = vote_dict[title]['time']
    y_axis = vote_dict[title]['proportion']
    regr.fit(x_axis, y_axis)

    # 최소값은 0 최대값은 100으로 설정
    for minute in range(60*24):
        predict_proportion = int(regr.predict(minute))
        if predict_proportion > 100:
            predict_proportion = 100
        elif predict_proportion < 0:
            predict_proportion = 0

        item = [minute, title, predict_proportion]
        db_cursor.execute('INSERT INTO lineup_predictproportion(time, title, proportion) VALUES (?,?,?)', item)
        time.sleep(0.01) # sqlite write time limite 방지
        
    #(title, time, proprotion)
    print regr.coef_
db_connector.commit()
db_connector.close()



