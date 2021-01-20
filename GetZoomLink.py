#!/usr/bin/python3
# Coded while I was high on 300 mg of caffeine
# Proudly speedcoded by Brandon Yao

import datetime
import json
import os
from os import path

# no school = 1, minimum day = 2, regular = 3
# delete config.json if you need to change zoom links
# if this starts acting up contact me


def convert_format(date, originalFormat):
    ret = datetime.datetime.strptime(date, originalFormat)
    ret.strftime("%d/%m/%Y")
    return ret


def get_day_type():
    # opens dates.json file
    with open("dates.json") as f:
        data = json.load(f)
        dateData = data["Dates"]
        breakData = data["Breaks"]
        if(datetime.datetime.today().weekday() > 4):
            return 1
        today = datetime.datetime.now().strftime("%A %B %d %Y")
        # checks if key(today) is in the dictionary
        if(today in dateData[0]):
            # all this basically just returns 1 or 2 based on dictionary
            day = dateData[0][today].lower()
            if(day.find("no school") > 0):
                return 1
            elif(day.find("minimum") > 0):
                return 2
        # formats today to help with comparison
        # for some reason doing directly returns string instead of date
        today = convert_format(today, "%A %B %d %Y")
        # iterates through each dict in breaks
        for i in range(len(breakData)):
            # returns dictionary of current list
            breakRange = list(breakData[i])
            # formats the start and end dates of break to help with comparison
            start = convert_format(breakRange[0], "%B %d %Y")
            end = convert_format(breakRange[1], "%B %d %Y")
            # checks if today is between the start and end dates
            if(start <= today <= end):
                return 1
        # default case, returns 3 for normal
        return 3


def get_link(currentDay, dayType):
    # tbh I don't even remember how or why this works, I just know I used recursion
    with open("config.json") as f:
        days = json.load(f)['Days']
        if(dayType == 1):
            return "No school today"
        elif(dayType == 2):
            return days
        if(currentDay < 3):
            return days[0][f'{currentDay}']
        return get_link(currentDay-3, dayType)

# Is called when


def request_links():
    # checks if needs to write new config.json
    print("\033[31;1m!!!REMEMBER TO OPEN README.txt BEFORE USING!!!\033[0m")
    # gets inputs to populate config.json
    while True:
        monday = input("Enter your links for Monday and Thursday: ")
        tuesday = input("Enter your links for Tuesday and Friday: ")
        wednesday = input("Enter your links for Wednesday: ")
        # checks if any link is empty
        if("" in [monday, tuesday, wednesday]):
            # asks again for user input
            print("\nNot enough zoom links found")
            if(input("Would you like to retry?: ") in 'yes'):
                continue
            # tells config.json file to use default
            else:
                print("No zoom links will be used")
                break
        break
        # opens file at path '.', 'w+' means read and write
    days = json.dumps(
        {'Days': [{'0': monday, '1': tuesday, '2': wednesday}]})
    f = open(os.path.join(".", "config.json"), 'w+')
    f.write(days)


today = datetime.datetime.today().weekday()
if(not path.exists("config.json")):
    request_links()
print(get_link(today, get_day_type()))
