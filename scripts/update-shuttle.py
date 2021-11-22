import sys
import apiController
import apiHandler
import ast
import datetime
from time import sleep
def main():
    try:
        time = sys.argv[1]
        station = ast.literal_eval(sys.argv[2])
        
        result = []
     
        day = apiController.weekDay(datetime.datetime.now())
        local_path = "/root/shuttle-data/%s/%s/data" % (day, time)
        remote_path = "%s/%s/data" % (day, time)
    
        for i in range(len(station) - 1):
            url = apiHandler.NAVER_ENDPOINT() % (station[i][1], station[i][0], station[i + 1][1], station[i + 1][0])
            time_sec = apiController.getRoadInfo(url) // 1000
            result.append(time_sec)
            print("worked, sleeping")
            sleep(time_sec)


        apiController.downloadS3(local_path, remote_path, "shuttle-data")

        # read local DB
        with open(local_path, "r") as fp:
            datas = fp.readlines()
            if datas != None and len(datas) > 0:
                datas = datas.split(",")
                count = int(datas[-1])
                datas = list(map(int, datas))
            
                # update DB values
                for i in range(len(result) - 1):
                    result[i] = ((datas[i] * count) + result[i]) // (count + 1)
            else: 
                count = 0


        # write local DB
        with open(local_path, "w") as fp:
            fp.write(",".join(map(str, result)))
            fp.write("," + str(count + 1))
    
        apiController.uploadS3(local_path, remote_path, "shuttle-data")
        print(" * [%s] subProgram Finished" % (time))
    except Exception as e:
        print(" * Error in update-shuttle subProgram => ", e)

if __name__ == "__main__":
    main()
