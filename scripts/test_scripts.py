import apiHandler
import apiController
import unittest

class apiTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_bus(self):
        bus = apiHandler.BUS_KEY()
        self.assertIsNotNone(bus)
        endpoint = apiHandler.BUS_ENDPOINT()
        self.assertEqual(endpoint % (10, 20), "http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList?serviceKey=10&stationId=20")

    def test_holiday(self):
        holiday = apiHandler.HOLIDAY_KEY()
        self.assertIsNotNone(holiday)
        endpoint = apiHandler.HOLIDAY_ENDPOINT()
        self.assertEqual(endpoint % (10, 20, 30),"http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?serviceKey=10&solYear=20&solMonth=30")

    def test_naver(self):
        n_key = apiHandler.NAVER_KEY()
        n_id = apiHandler.NAVER_ID()
        self.assertIsNotNone(n_key)
        self.assertIsNotNone(n_id)
        endpoint = apiHandler.NAVER_ENDPOINT()
        self.assertEqual(endpoint % (1, 1, 2, 2), "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start=1,1&goal=2,2&option=trafast")

    def test_ncloud(self):
        secret = apiHandler.NCLOUD_SECRET_KEY()
        access = apiHandler.NCLOUD_ACCESS_KEY()

        self.assertIsNotNone(secret)
        self.assertIsNotNone(access)

    
    def test_isWeekend(self):
        import datetime
        now = datetime.datetime.now()

        weekend = 0
        for i in range(0, 7):
            if apiController.isWeekend(now + datetime.timedelta(days = i), []):
                weekend += 1

        self.assertEqual(weekend, 2)



if __name__ == "__main__":
    unittest.main(verbosity=3)
