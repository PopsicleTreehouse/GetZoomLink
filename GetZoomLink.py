#!/usr/bin/python3
# @TODO: Check for grade level, only print if grade level matches

import json
import re
import tkinter as tk
import webbrowser
from datetime import datetime

TK_SILENCE_DEPRECATION = 1


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, height=600, width=600)
        try:
            f = open('config.json')
            f.close()
        except FileNotFoundError:
            self.times = []
            self.days = []
            self.dLabel = tk.Label(
                self, text="Links", fg='black')
            self.dLabel.pack(side=tk.LEFT)
            self.dEntry = tk.Entry(self)
            self.dEntry.pack(side=tk.LEFT)
            dSubmit = tk.Button(self, text='Submit',
                                width=10, command=lambda: self.callback(True))
            dSubmit.pack(side=tk.LEFT)
            self.tLabel = tk.Label(
                self, text="Times", fg='black')
            self.tLabel.pack(side=tk.LEFT)
            self.tEntry = tk.Entry(self)
            self.tEntry.pack(side=tk.LEFT)
            tSubmit = tk.Button(self, text='Submit',
                                width=10, command=lambda: self.callback(False))
            tSubmit.pack(side=tk.LEFT)
            # json.dump(
            #     {'Days': self.days, 'Times': self.times}, output, ensure_ascii=False)
        button1 = tk.Button(self, text='Get Link', command=lambda: self.get_link(
            datetime.today().weekday(), self.get_day_type()), fg='black')
        button1.pack(side=tk.LEFT)

    def format_url(self, url):
        if(not re.match('(?:http|ftp|https)://', url)):
            return 'http://{}'.format(url)
        return url

    def convert_format(self, date, originalFormat):
        ret = datetime.strptime(date, originalFormat)
        ret.strftime("%d/%m/%Y")
        return ret

    def get_day_type(self):
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
            today = self.convert_format(today, "%A %B %d %Y")
            for i in range(len(breakData)):
                breakRange = list(breakData[i])
                start = self.convert_format(breakRange[0], "%B %d %Y")
                end = self.convert_format(breakRange[1], "%B %d %Y")
                if(start <= today <= end):
                    return 1
            return 3

    def get_link(self, currentDay, dayType):
        now = datetime.today().now().strftime('%H%M')
        with open("config.json") as config:
            elements = json.load(config)
            times = elements["Times"]
            days = elements["Days"]
            if(dayType == 1):
                return "No school today"
            elif(dayType == 2):
                return days
            index = 0
            for i in range(len(times)):
                if(i >= len(days[currentDay])):
                    break
                if(int(times[i]) >= int(now)):
                    index = i
                    break
            if(currentDay < 3):
                label = tk.Label(
                    self, text="Your current link is: \""+days[currentDay].split(' ')[index]+"\"", highlightbackground='#3E4149')
            else:
                label = tk.Label(
                    self, text="Your current link is: \""+days[currentDay-3].split(' ')[index]+"\"", highlightbackground='#3E4149')
            label.pack()

    def callback(self, isDay):
        with open('config.json', 'w') as output:
            if(isDay):
                self.days.append(self.dEntry.get())
            else:
                self.times.append(self.tEntry.get())
            self.dEntry.delete(0, 'end')
            self.tEntry.delete(0, 'end')
            json.dump(
                {'Days': self.days, 'Times': self.times}, output, ensure_ascii=False)


def main():
    root = tk.Tk()
    root.geometry("550x40")
    root.title("GetZoomLink.py")
    root.resizable(width=False, height=False)
    App(root).pack(expand=True, fill='both')
    root.mainloop()


if __name__ == '__main__':
    main()
