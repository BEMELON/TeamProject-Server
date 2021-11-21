import apiHandler
import datetime

def getHoliday(year: str, month: str) -> list:
    import xml.etree.ElementTree as elemTree

    endPoint = apiHandler.HOLIDAY_ENDPOINT()
    key = apiHandler.HOLIDAY_KEY()

    try:
        res = requests.get(endPoint % (key, year, month))
        tree = elemTree.fromstring(res.text)
        holidays = tree.find("./body").find("./items").findall("./item")

        result = []
        for holiday in holidays:
            result.append(holiday.find("./locdate").text[-2:])

        return result
    except:
        return []


def isWeekend(now: datetime, holiday: list) -> bool:
    return now.weekday() > 4 or now.day in holiday

def weekDay(day):
    return ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"][day.weekday()]

def getRoadInfo(url:str) -> int:
    import json

    NAVER_SECRET_KEY = apiHandler.NAVER_KEY()
    NAVER_CLIENT_ID = apiHandler.NAVER_ID()

    http = urllib3.PoolManager()
    response = http.request('GET', url, headers={ "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID, "X-NCP-APIGW-API-KEY": NAVER_SECRET_KEY})

    json_object = json.loads(response.data.decode('utf-8'))
    targets = json_object["route"]["trafast"][0]["guide"]

    part_sum = 0
    for target in targets:
        part_sum += int(target['duration'])

    return part_sum


def downloadS3(local_path: str, remote_path: str, service: str):
    import boto3
    S3_ACCESS_KEY = apiHandler.NCLOUD_ACCESS_KEY()
    S3_SECRET_KEY = apiHandler.NCLOUD_SECRET_KEY()

    s3 = boto3.client(service, 
                      endpoint_url = "https://kr.object.ncloudstorage.com",
                      aws_access_key_id = S3_ACCESS_KEY,
                      aws_secret_access_key = S3_SECRET_KEY)

    s3.download_file(service, remote_path, local_path)


def uploadS3(local_path: str, remote_path: str, service: str):
    import boto3

    S3_ACCESS_KEY = apiHandler.NCLOUD_ACCESS_KEY()
    S3_SECRET_KEY = apiHandler.NCLOUD_SECRET_KEY()

    s3 = boto3.client(service, 
                      endpoint_url = "https://kr.object.ncloudstorage.com",
                      aws_access_key_id = S3_ACCESS_KEY,
                      aws_secret_access_key = S3_SECRET_KEY)

    s3.upload_file(local_path, service, remote_path)




