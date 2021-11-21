import datetime
import subprocess
import json
import time
import os
import apiHandler
import apiController
import dataHandler

holiday_year = 0
holiday_month = 0
holiday_table = []

"""
stationInfo = {
    "명지대": [37.224283500000006, 127.18728609999998],
    "상공회의소":[37.230680400000004, 127.1882456],
    "진입로": [37.23399210000001,  127.18882909999999],
    "명지대역": [37.238513300000015, 127.18960559999998],
    "진입로(명지대방향)": [37.233999900000015, 127.18861349999999],
    "이마트": [37.23036920601031 , 127.18799722805205],
    "명진당": [37.22218358841614, 127.18895343450612],
    "제3공학관": [37.219509212602546, 127.1829915220452],
    "동부경찰서": [37.23475516860965 , 127.19817660622552],
    "용인시장": [37.235430174474516, 127.20667763142193],
    "중앙공영주차장": [37.23391585619981 , 127.20892718244508],
    "제1공학관": [37.22271140883418, 127.18678412115244]
}
mju_stations = ["명지대", "상공회의소", "진입로", "명지대역", "진입로(명지대방향)", "이마트", "명진당", "제3공학관"]
ctiy_stations = ["명지대", "상공회의소", "진입로", "진입로(명지대방향)", "이마트", "동부경찰서", "용인시장", "중앙공영주차장", "제1공학관", "제3공학관"]
NAVER_endPoint = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
NAVER_SRC = "?start="
NAVER_DEST = "&goal="
NAVER_OPTION = "&option=trafast"

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
access_key = 'tvJAOigh9hYG22mBG92k'
secret_key = 'jORTSNnk6954dULOb0XQOcornNZv0JdlA1d9WVVj'
def weekDay(day):
    return ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"][day.weekday()]

def getRoadInfo(url):
    NAVER_SECRETKEY = "MgLSNKb2EsLXMPYq0Ailk5iFa3gWbKxIBl20DIm4"
    NAVER_CLIENT_ID = "p4xiv96tkc"
    http = urllib3.PoolManager()
    response = http.request('GET', url, headers={ "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID, "X-NCP-APIGW-API-KEY": NAVER_SECRETKEY})

    json_object = json.loads(response.data.decode('utf-8'))
    targets = json_object["route"]["trafast"][0]["guide"]
    part_sum = 0
    for target in targets:
        part_sum += int(target['duration'])
    return part_sum


def getHoliday(year, month):
    endPoint = r"http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    serviceKey = r"ZJF99uIbDjNnsZBlrbDg%2BDL%2FCyHI2Vc%2BATgI41upeL1%2FGf2jjy8keoY%2FEb6E6CLtokViU7v8bN8tRY0vJ2x3EQ%3D%3D"
    url = endPoint + r"?serviceKey=" + serviceKey + r"&solYear=" + str(year) + r"&solMonth=" + str(month)

    res = requests.get(url)
    tree = elemTree.fromstring(res.text)
    holidays = tree.find("./body").find("./items").findall("./item")

    result = []
    for holiday in holidays:
        result.append(holiday.find("./locdate").text[-2:])

    return result

"""

def main():
    holiday_year = 0
    holiday_month = 0
    holiday_table = []
    while True:
        now = datetime.datetime.now()
        year =  str(now.year)
        month = now.month if now.month > 9 else "0" + str(now.month)
        day = str(now.day)
        hour = str(now.hour) if now.hour > 9 else "0" + str(now.hour)
        minute = str(now.minute) if now.minute > 9 else "0" + str(now.minute)
        second = str(now.second) if now.second > 9 else "0" + str(now.second)
        print(" * [%s/%s/%s] %s:%s:%s start!" % (year, month, day, hour, minute, second)) 
        
        if holiday_year != year or holiday_month != month:
            holiday_year = year
            holiday_month = month
            holiday_table = apiController.getHoliday(year, month)
            
      
        curr_time = ":".join([hour, minute])
        if apiController.isWeekend(now, holiday_table): # Weekend
            if curr_time in dataHandler.MJU_CITY_WEEKEND_TIMETABLE():
                print(" * [%s:%s, WEEKEND, CITY] Event dispatched!" % (hour, minute)) 
                timeTable = dataHandler.MJU_CITY_WEEKEND_TIMETABLE()
                station = dataHandler.MJU_CITY_COOR()
        else: # Weekday
            if curr_time in dataHandler.MJU_CITY_WEEKDAY_TIMETABLE():
                print(" * [%s:%s, WEEKDAY, CITY] Event dispatched!" % (hour, minute)) 
                timeTable = dataHandler.MJU_CITY_WEEKDAY_TIMETABLE()
                station = dataHandler.MJU_CITY_COOR()
            elif curr_time in dataHandler.MJU_STATION_WEEKDAY_TIMETABLE():
                print(" * [%s:%s, WEEKDAY, STATION] Event dispatched!" % (hour, minute))
                timeTable = dataHandler.MJU_STATION_WEEKDAY_TIMETABLE()
                station = dataHandler.MJU_STATION_COOR()
            else:
                timeTable = station = None
                
        
        if timeTable is not None and station is not None:
            os.system("python update.py \"%s\" \"%s\"" % (curr_time, str(station)))
                
    
        time.sleep(59)
    
    
main()
"""
    
    if now.weekday() > 4 or day in holiday_table:
        # 주말
        timeTable = ["8:20", "9:20", "10:20", "11:20", "12:20", "13:20", "15:20", "16:20", "17:20", "18:00"]
        if curr_time in timeTable:
            print("\t * Weekend, routine started!")
            pid = os.fork()
            if not pid:
                result = []
                for i in range(len(ctiy_stations) - 1):
                    url = NAVER_endPoint + NAVER_SRC + str(stationInfo[city_stations[i]][1]) + "," + str(stationInfo[city_stations[i]][0]) + NAVER_DEST + str(stationInfo[city_stations[i+1]][1]) + "," + str(stationInfo[city_stations[i+1]][0]) + NAVER_OPTION
                    timeRequire = (getRoadInfo(url) // 1000) # to SEC
                    result.append(timeRequire // 60) # to MIN
                    time.sleep(timeRequire)

                local_path = "data/" + weekDay(now) + "/" + curr_time + "/info.json"
                remote_path = weekDay(now) + "/" + curr_time + "/info.json"

                # download DB file
                s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
                s3.download_file("mba-busdata", remote_path, local_path)
                with open(local_path, "r") as fp:
                    datas = fp.readlines()
                if datas != None and len(datas) > 0:
                    datas = datas.split(",")
                    count = int(datas[-1])
                    datas = list(map(int, datas))
                    # update DB values
                    for i in range(len(result)):
                        result[i] = ((datas[i] * count) + result[i]) // (count + 1)
                else: 
                    count = 0

                # write local file
                with open(local_path, "w") as fp:
                    print(result)
                    fp.write(",".join(map(str, result)))
                    fp.write("," + str(count + 1))
                
                # upload DB file
                s3.upload_file(local_path, "mba-busdata", remote_path)
                print("\t * Weekend, " + curr_time + " routine Finished!")
                exit()
    else:
        # 평일
        station_timeTable = ["8:00", "8:15", "8:20", "8:35", "8:45", "9:00", "9:15", "9:30", "9:35", "9:40", "9:55", "10:20", "10:30", "10:45", "11:00", "11:25", "11:45", "11:55", "12:05", "12:30", "12:45", "13:25", "13:40", "14:00", "14:10", "14:30", "14:50", "15:00", "15:10", "15:25", "15:55", "16:10", "16:25", "16:50", "17:00", "17:10", "17:20", "17:45", "18:00", "19:00", "19:20", "19:30"]
        city_timeTable = ["8:05", "8:55", "10:10", "11:20", "13:10", "14:20", "15:40", "16:35", "18:10", "20:00"]

        flag = False
        if curr_time in station_timeTable:
            print(" * weekday, station, routine started!")
            stations = mju_stations
            flag = True
        elif curr_time in city_timeTable:
            print(" * weekday, city, routine started!")
            stations = ctiy_stations
            flag = True

        if flag:
            pid = os.fork()
            if not pid:
                result = []
                for i in range(len(stations) - 1):
                    url = NAVER_endPoint + NAVER_SRC + str(stationInfo[stations[i]][1]) + "," + str(stationInfo[stations[i]][0]) + NAVER_DEST + str(stationInfo[stations[i+1]][1]) + "," + str(stationInfo[stations[i+1]][0]) + NAVER_OPTION
                    timeRequire = (getRoadInfo(url) // 1000) # to SEC
                    result.append(timeRequire // 60) # to MIN
                    time.sleep(timeRequire)

                local_path = "data/" + weekDay(now) + "/" + curr_time + "/info.json"
                remote_path = weekDay(now) + "/" + curr_time + "/info.json"
                # write to DB
                # download DB file
                s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
                s3.download_file("mba-busdata", remote_path, local_path)
                with open(local_path, "r") as fp:
                    datas = fp.readlines()
                if datas != None and len(datas) > 0:
                    datas = datas.split(",")
                    count = int(datas[-1])
                    datas = list(map(int, datas))
                    # update DB values
                    for i in range(len(result)):
                        result[i] = ((datas[i] * count) + result[i]) // (count + 1)
                else:
                    count = 0

                # write local file
                with open(local_path, "w") as fp:
                    print(result)
                    fp.write(",".join(map(str, result)))
                    fp.write("," + str(count + 1))
                
                # upload DB file
                s3.upload_file(local_path, "mba-busdata", remote_path)
                print("\t * Weekday, " + curr_time + " routine Finished!")
                exit()
    time.sleep(55)
    """




