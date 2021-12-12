import dataHandler
import math
import apiHandler
import apiController

station = dataHandler.MJU_STATION_COOR()

myStation = []

for i in range(len(station)):
    if i == 4:
       myStation.append([37.23874059999999, 127.18622570000005])
    myStation.append(station[i])

print(myStation)

for i in range(len(station) - 1):
    url = apiHandler.NAVER_ENDPOINT() % (station[i][1], station[i][0], station[i+1][1], station[i+1][0])
    print(math.ceil(apiController.getRoadInfo(url) // 1000 / 60))

print("NEXT")
station = myStation
for i in range(len(station) - 1):
    url = apiHandler.NAVER_ENDPOINT() % (station[i][1], station[i][0], station[i+1][1], station[i+1][0])
    print(math.ceil(apiController.getRoadInfo(url) // 1000 / 60))

