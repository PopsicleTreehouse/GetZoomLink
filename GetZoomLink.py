#!/usr/bin/python3
import json
import tkinter as tk
from datetime import datetime
from functools import partial
from itertools import chain


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, height=900, width=600)
        self.createdJson = False
        self.manual = False
        try:
            f = open("config.json")
            f.close()
            self.create_btn()
        except FileNotFoundError:
            self.times = []
            self.links = []
            self.entryLabel = tk.Label(
                self, text="Link Monday", fg="black")
            self.entryLabel.pack(side=tk.LEFT)
            self.entry = tk.Entry(self)
            self.entry.pack(side=tk.LEFT)
            self.Submit = tk.Button(
                self, text="Submit", width=10, command=lambda: self.callback(True, 0))
            self.Submit.pack(side=tk.LEFT)
            self.manualCheckbox = tk.Checkbutton(
                self, text="Manual period selection", variable=self.manual)
            self.manualCheckbox.pack(side=tk.LEFT)
            self.createdJson = True
            self.confirm = tk.Button(
                self, text="Get link", command=lambda: self.create_btn(confirm=True))
            self.confirm.pack()

    def create_btn(self, confirm=False):
        try:
            if(confirm):
                self.confirm.destroy()
            if(self.createdJson):
                self.destroy_items(
                    [self.Submit, self.entryLabel, self.entry, self.manualCheckbox])
            with open("config.json") as f:
                self.linkLabel = tk.Label(
                    self, highlightbackground="#3E4149", fg="black")
                self.linkLabel.pack()
                config = json.load(f)
                self.manual = config["manual"]
                if(self.manual):
                    lnk = list(chain.from_iterable(config["links"]))
                    for i in range(len(lnk)-1):
                        pButton = tk.Button(self, text="Period " + str(i+1), command=partial(self.get_link, datetime.today().weekday(), self.get_day_type(), period=i),
                                            fg="black")
                        pButton.pack(side=tk.LEFT)
                    access = tk.Button(self, text="Access", command=lambda: self.get_link(datetime.today().weekday(), self.get_day_type(), period=len(lnk)-1),
                                       fg="black")
                    access.pack(side=tk.LEFT)
                else:
                    copy = tk.Button(self, text="Copy Link", command=lambda: self.get_link(datetime.today().weekday(), self.get_day_type()),
                                     fg="black")
                    copy.pack(side=tk.LEFT)

        except FileNotFoundError:
            self.confirm.config(text="Fuck")

    def destroy_items(self, items):
        for i in items:
            i.destroy()

    def callback(self, isDay, day):
        with open("config.json", "w") as output:
            days = ["Links Monday", "Links Tuesday", "Links Wednesday"]
            if isDay:
                self.links.append(self.entry.get().split(" "))
            else:
                self.times.append(self.entry.get())
            self.entry.delete(0, "end")
            if day < 2:
                self.Submit.config(
                    command=lambda: self.callback(True, day+1))
                self.entryLabel.config(text=days[day+1])
            else:
                self.Submit.config(command=lambda: self.callback(False, day))
                self.entryLabel.config(text="Times")
            json.dump({"links": self.links, "times": self.times, "manual": self.manual},
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
            dateData = data["dates"]
            breakData = data["breaks"]
            today = datetime.now().strftime("%A %B %d %Y")
            day = today
            if today in dateData[0]:
                day = dateData[0][today].lower()
            today = self.convert_format(today, "%A %B %d %Y")
            for i in range(len(breakData)):
                breakRange = list(breakData[i])
                start = self.convert_format(breakRange[0], "%B %d %Y")
                end = self.convert_format(breakRange[1], "%B %d %Y")
                if start <= today <= end:
                    day = breakData[i][end.strftime("%B %d %Y")].lower()
            if day.find("no school") > 0:
                return 1
            elif day.find("minimum") > 0:
                return 2
            return 3

    def get_link(self, currentDay, dayType, period=None):
        now = datetime.today().now().strftime("%H%M")
        with open("config.json") as config:
            elements = json.load(config)
            times = elements["times"]
            links = elements["links"]
            if currentDay >= 3:
                currentDay = currentDay - 3
            # takes closest number to current time as index
            index = min(range(len(times)), key=lambda i: abs(
                int(times[i]) - int(now)))
            if(currentDay == 2):
                index = 0
            currentPeriod = links[currentDay][index]
            if(self.manual):
                currentPeriod = list(chain.from_iterable(links))[period]
            labels = ["No school today", links,
                      "Next link: \""+currentPeriod+"\""]
            labelText = labels[dayType-1]
            self.clipboard_clear()
            self.clipboard_append(currentPeriod)
            self.linkLabel.config(text=labelText)


def main():
    root = tk.Tk()
    root.geometry("800x80")
    root.title("GetZoomLink.py")
    root.resizable(width=True, height=False)
    App(root).pack(expand=True, fill="both")
    root.mainloop()


if __name__ == "__main__":
    main()
