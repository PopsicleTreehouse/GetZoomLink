#!/usr/bin/python3
# @TODO: Check for grade level, only print if grade level matches

import json
import sys
from datetime import datetime
from os import path


def convert_format(date, originalFormat):
    ret = datetime.strptime(date, originalFormat)
    ret.strftime("%d/%m/%Y")
    return ret


def get_day_type():
    if(datetime.today().weekday() > 4):
        return 1
    with open("dates.json") as f:
        data = json.load(f)
        dateData = data["Dates"]
        breakData = data["Breaks"]
        today = datetime.now().strftime("%A %B %d %Y")
        if(today in dateData[0]):
            day = dateData[0][today].lower()
            if(day.find("no school") > 0):
                return 1
            elif(day.find("minimum") > 0):
                return 2
        today = convert_format(today, "%A %B %d %Y")
        for i in range(len(breakData)):
            breakRange = list(breakData[i])
            start = convert_format(breakRange[0], "%B %d %Y")
            end = convert_format(breakRange[1], "%B %d %Y")
            if(start <= today <= end):
                return 1
        return 3


def get_link(currentDay, dayType, times):
    print(times)
    now = datetime.today().now().strftime('%H%M')
    with open("config.json") as config:
        days = json.load(config)['Days']
        if(dayType == 1):
            return "No school today"
        elif(dayType == 2):
            return days
        for i in range(len(times)):
            index = len(days[currentDay])-1
            if(times[i] >= int(now)):
                print(i)
                index = i
                break
        if(currentDay < 3):
            return days[currentDay][index]
        else:
            return days[currentDay-3][index]


def create_config():
    with open('config.json', 'w') as output:
        while True:
            days = []
            days.append((
                input("Enter your links for Monday and Thursday: ")).split(' '))
            days.append(
                (input("Enter your links for Tuesday and Friday: ")).split(' '))
            days.append(
                (input("Enter your links for Wednesday: ")).split(' '))
            if("" in days):
                print("\nNot enough zoom links found")
                if(input("Would you like to retry?: ") in 'yes'):
                    continue
                else:
                    print("One or more days will be missing a zoom link")
                    break
            json.dump(
                {'Days': days}, output, ensure_ascii=False)
            return


if(not path.exists("config.json")):
    create_config()

results = list(int(i) for i in sys.argv[1:])

print(get_link(datetime.today().weekday(),
               get_day_type(), results))
