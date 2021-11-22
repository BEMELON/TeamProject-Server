import datetime
import subprocess
import json
import time
import os
import apiHandler
import apiController
import dataHandler

# -*- coding: utf-8 -*-
holiday_year = 0
holiday_month = 0
holiday_table = []

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
            subprocess.Popen(["python3", "update-shuttle.py", curr_time, str(station)])
                
        subprocess.Popen(["python3", "update-bus.py"])
        time.sleep(60)
    
    
main()
