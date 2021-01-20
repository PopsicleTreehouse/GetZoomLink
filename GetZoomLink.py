#!/usr/bin/python3
from datetime import datetime
import json
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


def get_link(currentDay, dayType):
    with open("config.json") as config:
        days = json.load(config)['Days']
        if(dayType == 1):
            return "No school today"
        elif(dayType == 2):
            return days
        if(currentDay < 3):
            return days[0][currentDay]
        else:
            return days[0][currentDay-3]


def request_links():
    with open('config.json', 'w') as output:
        while True:
            days = []
            days.append(input("Enter your links for Monday and Thursday: "))
            days.append(input("Enter your links for Tuesday and Friday: "))
            days.append(input("Enter your links for Wednesday: "))
            grade = int(input("What's your grade level? 1-12: "))
            if("" in days):
                print("\nNot enough zoom links found")
                if(input("Would you like to retry?: ") in 'yes'):
                    continue
                else:
                    print("One or more days will be missing a zoom link")
                    break
            json.dump(
                {'Days': [days], 'Grade': grade}, output, ensure_ascii=False)
            return


if(not path.exists("config.json")):
    request_links()
print(get_link(datetime.today().weekday(), get_day_type()))
