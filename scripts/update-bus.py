import apiHandler
import apiController
import xml.etree.ElementTree as elemTree
import datetime
import requests 

stationID = "228002023"
target = ["228000182", "228000177", "228000174"]


def getArrivalList(url):
    res = requests.get(url)
    tree = elemTree.fromstring(res.text)

    body = tree.find('msgBody')
    if body is None: return []
    else: return body.findall("busArrivalList")


def main():
    BUS_KEY = apiHandler.BUS_KEY()
    BUS_ENDPOINT = apiHandler.BUS_ENDPOINT() % (BUS_KEY, stationID)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    day = apiController.weekDay(now)

    local_path = "/root/bus-data/%s/info" % (day)
    remote_path = "%s/info" % (day)
    
    for bus in getArrivalList(BUS_ENDPOINT):
        routeID = bus.find('routeId').text
        if routeID in target and int(bus.find("predictTime1").text) <= 1:
                apiController.downloadS3(local_path, remote_path, "bus-data")
                with open(local_path, "a") as fp:
                    fp.write(",%s" % current_time)

                apiController.uploadS3(local_path, remote_path, "bus-data")



if __name__ == "__main__":
    main()

