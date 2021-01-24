#!/usr/bin/python3
# @TODO: Check for grade level, only print if grade level matches

import json
import tkinter as tk
from datetime import datetime


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, height=600, width=600)
        self.createdJson = False
        try:
            f = open("config.json")
            f.close()
        except FileNotFoundError:
            self.times = []
            self.days = []
            self.entryLabel = tk.Label(self, text="Link Monday", fg="black")
            self.entryLabel.pack(side=tk.LEFT)
            self.entry = tk.Entry(self)
            self.entry.pack(side=tk.LEFT)
            self.Submit = tk.Button(
                self, text="Submit", width=10, command=lambda: self.callback(True, 0))
            self.Submit.pack(side=tk.LEFT)
            self.createdJson = True
        button1 = tk.Button(self, text="Copy Link", command=lambda: self.get_link(datetime.today().weekday(), self.get_day_type()),
                            fg="black")
        button1.pack(side=tk.LEFT)
        self.label = tk.Label(self, highlightbackground="#3E4149", fg="black")
        self.label.pack()

    def destroy_items(self, items):
        for i in items:
            i.destroy()

    def callback(self, isDay, day):
        with open("config.json", "w") as output:
            days = ["Links Monday", "Links Tuesday", "Links Wednesday"]
            if isDay:
                self.days.append(self.entry.get().split(" "))
            else:
                self.times.append(self.entry.get())
            self.entry.delete(0, "end")
            if(day < 2):
                self.Submit.config(
                    command=lambda: self.callback(True, day+1))
                self.entryLabel.config(text=days[day+1])
            else:
                self.Submit.config(command=lambda: self.callback(False, day))
                self.entryLabel.config(text="Times")
            json.dump({"Days": self.days, "Times": self.times},
                      output, ensure_ascii=False)

    def convert_format(self, date, originalFormat):
        ret = datetime.strptime(date, originalFormat)
        ret.strftime("%d/%m/%Y")
        return ret

    def get_day_type(self):
        if datetime.today().weekday() > 4:
            return 1
        with open("dates.json") as f:
            data = json.load(f)
            dateData = data["Dates"]
            breakData = data["Breaks"]
            today = datetime.now().strftime("%A %B %d %Y")
            if today in dateData[0]:
                day = dateData[0][today].lower()
                if day.find("no school") > 0:
                    return 1
                elif day.find("minimum") > 0:
                    return 2
            today = self.convert_format(today, "%A %B %d %Y")
            for i in range(len(breakData)):
                breakRange = list(breakData[i])
                start = self.convert_format(breakRange[0], "%B %d %Y")
                end = self.convert_format(breakRange[1], "%B %d %Y")
                if start <= today <= end:
                    return 1
            return 3

    def get_link(self, currentDay, dayType):
        now = datetime.today().now().strftime("%H%M")
        with open("config.json") as config:
            elements = json.load(config)
            times = elements["Times"]
            days = elements["Days"]
            if currentDay >= 3:
                currentDay = currentDay - 3
            index = times.index(
                times[min(range(len(times)), key=lambda i: abs(int(times[i]) - int(now)))])
            labelText = "Next link: \""+days[currentDay][index]+"\""
            if dayType == 1:
                labelText = "No school today"
            elif dayType == 2:
                labelText = days
            if self.createdJson:
                self.destroy_items(
                    [self.Submit, self.entryLabel, self.entry])
            self.clipboard_clear()
            self.clipboard_append(labelText)
            self.label.config(text=labelText)


def main():
    root = tk.Tk()
    root.geometry("800x40")
    root.title("GetZoomLink.py")
    root.resizable(width=False, height=False)
    App(root).pack(expand=True, fill="both")
    root.mainloop()


if __name__ == "__main__":
    main()
