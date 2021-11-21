import json
keyPath = "/root/apiKey.json"
keys = json.load(open(keyPath, "r"))

def NAVER_ID():
    return keys["naver_id"]

def NAVER_KEY():
    return keys["naver_key"]

def NAVER_ENDPOINT():
    return r"https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start=%s,%s&goal=%s,%s&option=trafast"


def NCLOUD_SECRET_KEY():
    return keys["ncloud_secret_key"]

def NCLOUD_ACCESS_KEY():
    return keys["ncloud_access_key"]

def HOLIDAY_KEY():
    return keys["holiday_key"]

def HOLIDAY_ENDPOINT():
    return r"http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?serviceKey=%s&solYear=%s&solMonth=%s"


def BUS_KEY():
    return keys["bus_key"]


def BUS_ENDPOINT():
    return r"http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList?serviceKey=%s&stationId=%s"




