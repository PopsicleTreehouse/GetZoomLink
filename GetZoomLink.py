#!/usr/bin/python3
# @TODO: Check for grade level, only print if grade level matches (regex?)
# @TODO: Fix mimimum day copy system
# @TODO: Update dates.json based on website

import json
import tkinter as tk
from datetime import datetime


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.calledAfterJSON = False
        try:
            f = open("config.json")
            f.close()
            self.create_btn()
        except FileNotFoundError:
            self.times = []
            self.links = []
            self.manual = tk.IntVar()
            self.entryLabel = tk.Label(
                self, text="Link P1", fg="black")
            self.entryLabel.pack(side=tk.LEFT)
            self.entry = tk.Entry(self)
            self.entry.pack(side=tk.LEFT)
            self.Submit = tk.Button(
                self, text="Submit", width=10, command=lambda: self.callback(True, 0))
            self.Submit.pack(side=tk.LEFT)
            self.manualCheckbox = tk.Checkbutton(
                self, text="Manual period selection", variable=self.manual)
            self.manualCheckbox.pack(side=tk.LEFT)
            self.calledAfterJSON = True
            self.confirm = tk.Button(
                self, text="Get link", command=self.create_btn)
            self.confirm.pack(side=tk.LEFT)

    def create_btn(self):
        if(hasattr(self, "manualCheckbox")):
            self.manualCheckbox.pack_forget()
        if(hasattr(self, "confirm")):
            self.confirm.destroy()
        if(self.calledAfterJSON):
            self.destroy_items(
                [self.Submit, self.entryLabel, self.entry])
        with open("config.json") as f:
            self.linkLabel = tk.Label(
                self, fg="black")
            self.linkLabel.pack()
            config = json.load(f)
            self.manual = config["manual"]
            if(self.manual):
                lnk = config["links"]
                for i in range(len(lnk)-1):
                    tk.Button(self, text="Period " + str(i+1), command=lambda i=i: self.display_link(self.get_day_type(), text="Period "+str(i+1), period=i),
                              fg="black").pack(side=tk.LEFT, padx=21-len(lnk))
                tk.Button(self, text="Access", command=lambda: self.display_link(self.get_day_type(), text="Access"),
                          fg="black").pack(side=tk.LEFT, padx=21-len(lnk))
            else:
                tk.Button(self, text="Copy Link", command=lambda: self.display_link(self.get_day_type()),
                          fg="black").pack(side=tk.LEFT)

    def destroy_items(self, items):
        for i in items:
            i.destroy()

    def callback(self, isDay, day=6):
        with open("config.json", "w") as output:
            try:
                if(hasattr(self, "warningLabel")):
                    self.warningLabel.destroy()
                if(isDay):
                    self.links.append(self.entry.get())
                else:
                    self.times.append(int(self.entry.get()))
            except ValueError:
                self.warningLabel = tk.Label(
                    self, text="Enter a time instead!", fg="black")
                self.warningLabel.pack()
            self.entry.delete(0, "end")
            if(day < 5):
                self.Submit.config(
                    command=lambda: self.callback(True, day=day+1))
                self.entryLabel.config(text="Link P" + str(day+2))
            elif(day == 5):
                self.Submit.config(
                    command=lambda: self.callback(True, day=day+1))
                self.entryLabel.config(text="Link Access")
            else:
                self.Submit.config(command=lambda: self.callback(False))
                self.entryLabel.config(text="Times")
            json.dump({"links": self.links, "times": self.times, "manual": self.manual.get()},
                      output, ensure_ascii=False, indent=4)

    def convert_format(self, date, originalFormat):
        ret = datetime.strptime(date, originalFormat)
        ret.strftime("%d/%m/%Y")
        return ret

    def get_day_type(self):
        if(datetime.today().weekday() > 4):
            return 1
        with open("dates.json") as f:
            data = json.load(f)
            dateData = data["dates"]
            breakData = data["breaks"]
            today = datetime.now().strftime("%A %B %d %Y")
            day = today
            if(today in dateData[0]):
                day = dateData[0][today].lower()
            today = self.convert_format(today, "%A %B %d %Y")
            for i in range(len(breakData)):
                breakRange = list(breakData[i])
                start = self.convert_format(breakRange[0], "%B %d %Y")
                end = self.convert_format(breakRange[1], "%B %d %Y")
                if(start <= today <= end):
                    day = breakData[i][end.strftime("%B %d %Y")].lower()
            if(day.find("no school") > 0):
                return 1
            elif(day.find("minimum") > 0):
                return 2
            return 3

    def display_link(self, dayType, text=None, period=6):
        now = datetime.today().now().strftime("%H%M")
        with open("config.json") as config:
            currentDay = datetime.today().weekday()
            elements = json.load(config)
            times = elements["times"]
            links = elements["links"]
            if(5 > currentDay >= 3):
                currentDay = currentDay - 3
            # takes closest number to current time as index from list
            linkIndex = [[0, 2, 4], [1, 3, 5], [0]]
            index = min(range(len(linkIndex[currentDay])), key=lambda i: abs(
                times[i] - int(now)))
            currentPeriod = links[linkIndex[currentDay][index]]
            if(currentDay == 2 and not self.manual):
                currentPeriod = links[6]
                text = "Access"
            if(self.manual):
                index = period
                currentPeriod = links[index]
                labelText = f"{text} Link: \"{currentPeriod}\""
            else:
                if(currentDay != 2):
                    text = "Period " + str(linkIndex[currentDay][index]+1)
                labels = ["No school today", links,
                          f"{text} Link: \"{currentPeriod}\""]
                labelText = labels[dayType-1]
            self.clipboard_clear()
            self.clipboard_append(currentPeriod)
            self.linkLabel.config(text=labelText)


def main():
    root = tk.Tk()
    root.minsize(800, 80)
    root.title("Get Zoom Link")
    App(root).pack(expand=True, fill="both")
    root.mainloop()


if(__name__ == "__main__"):
    main()
