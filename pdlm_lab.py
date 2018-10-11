#!/usr/bin/#!/usr/bin/env python3

# Pendulum Lab Data Processing Tool
# Copyright by Jerry Yan, 2018

import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math


class PdlmData:
    length = 0.0
    trials = []
    periods = 0.0
    # angleRange = 0

    def avgPeriod(self):
        try:
            trLen = len(self.trials)
            trSum = sum(self.trials)
            trSum = trSum / self.periods
            trAvg = trSum / trLen
        except ZeroDivisionError:
            trAvg = 0
        return trAvg

    def stdError(self):
        tr = [x / self.periods for x in self.trials]
        trLen = len(self.trials)
        dof = (trLen - 1) if trLen >= 2 else 1
        return stats.sem(tr, ddof=dof)


class PdlmDataSet:
    name = "Untitled"
    data = []

    def __init__(self, name="Untitled", open=False):
        self.name = name

    def fileName(self):
        return self.name + ".csv"

    def defaultFilePath(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        csvFilePath = os.path.join(dirname, self.fileName())
        return csvFilePath

    def openFrom(self, path="DEFAULT"):
        if path == "DEFAULT":
            csvPath = self.defaultFilePath()

        csvFile = open(csvPath, "r")
        dict_reader = csv.DictReader(csvFile)

        for row in dict_reader:
            dataRow = PdlmData()
            dataRow.length = float(row["length"])
            dataRow.trials = list(map(float, row["trials"].split(";")))
            dataRow.periods = float(row["periods"])
            self.data.append(dataRow)

        print("The data set has been successfully loaded from CSV file.")
        return

    def save(self, option=0):
        csvFile = open(self.defaultFilePath(), "w")

        fileheader = ["length", "trials", "periods", "avgPeriod", "stdError"]
        dict_writer = csv.DictWriter(csvFile, fileheader)

        dict_writer.writeheader()

        for row in self.data:
            dict_writer.writerow({"length": row.length, "trials": '; '.join(map(
                str, row.trials)), "periods": row.periods, "avgPeriod": round(row.avgPeriod(), 5), "stdError": round(row.stdError(), 5)})

        csvFile.close()
        print("File has been successfully saved.")
        return

    def delete(self, index):
        return

    def sortBy(self, sti=1):
        return

    def plot(self, option=1):
        if option == 1:
            x_data = self.listFromData("length")
            y_data = self.listFromData("avgPeriod")
            y_error = self.listFromData("stdError")
            plt.figure(1)
            plt.errorbar(x_data, y_data, yerr=y_error, fmt='ko', markersize=4, elinewidth=1)
            plt.xlabel("Length(cm)")
            plt.ylabel("Period(s)")
            plt.title(self.name + ": Length vs Period")
            plt.show()
            print("The plot has been successfully generated.")
        elif option == 2:
            x_data = self.listFromData("sqrtLength")
            y_data = self.listFromData("avgPeriod")
            y_error = self.listFromData("stdError")
            plt.figure(2)
            plt.errorbar(x_data, y_data, fmt='ko', markersize=4)
            plt.xlabel("sqrt[Length](cm^1/2)")
            plt.ylabel("Period(s)")
            plt.title(self.name + ": sqrt[Length] vs Period")
            plt.show()
            print("The plot has been successfully generated.")
        elif option == 3:
            x_data = self.listFromData("sqrtLength")
            y_data = self.listFromData("avgPeriod")
            y_error = self.listFromData("stdError")
            plt.figure(3)
            lFit = np.polyfit(x_data, y_data, 1)
            lFitP = np.poly1d(lFit)
            xp = np.linspace(min(x_data), max(x_data), 100)
            plt.errorbar(x_data, y_data, yerr=y_error, fmt='ko', markersize=4)
            plt.plot(xp, lFitP(xp), '--', label = "y=" + str(round(lFit[1],4)) + "x+" + str(round(lFit[0],4)))
            plt.xlabel("sqrt[Length](cm^1/2)")
            plt.ylabel("Period(s)")
            plt.title(self.name + ": sqrt[Length] vs Period w/ linear fit")
            plt.legend(loc="upper left")
            plt.show()
            print("The plot has been successfully generated.")

    def add(self, option=0):
        print("You initiated a new row of data.")
        data = PdlmData()
        while True:
            try:
                length = input("Enter the length in cm: ")
                data.length = float(length)
                break
            except ValueError:
                print("Invalid input. Please try again.")
        while True:
            try:
                trials = input("Enter the trials in s, separate by \",\": ")
                data.trials = list(map(float, trials.split(",")))
                break
            except ValueError:
                print("Invalid input. Please try again.")
        while True:
            try:
                periods = input("Enter the number of periods: ")
                data.periods = float(periods)
                break
            except ValueError:
                print("Invalid input. Please try again.")
        # angleRange = input("Enter the angle range in degrees: ")
        # data.angleRange = angleRange
        while True:
            try:
                confirm = input("Do you want to add this data? (y/n) ")
                if confirm == "y":
                    self.data.append(data)
                    print("Data has been saved.")
                elif confirm == "n":
                    print("Data not saved.")
                else:
                    raise Exception(1)
                break
            except Exception:
                print("Invalid choice. Please try again.")

    def listFromData(self, option):
        list = []
        if option == "length":
            list = [d.length for d in self.data]
        elif option == "avgPeriod":
            list = [d.avgPeriod() for d in self.data]
        elif option == "stdError":
            list = [d.stdError() for d in self.data]
        elif option == "sqrtLength":
            list = [math.sqrt(d.length) for d in self.data]
        return list


def initiate():
    print("----Pendulum Lab Data Processing Tool by Jerry Yan----")
    while True:
        opt = input(
            "Choose the following options: \n1 - Create a new data set \n2 - Open an existing data set \nYour choice: ")
        try:
            if opt == "1":
                newDataSet()
            elif opt == "2":
                openDataSet()
            else:
                raise Exception(1)
            break
        except Exception:
            print("Invalid choice. Please try again.")
        else:
            print("Unknown error. Please try again.")

def newDataSet():
    global set
    nm = input("Name the new data set: ")
    set = PdlmDataSet(nm)
    print("You created a new data set called " + set.name)

def openDataSet():
    global set
    nm = input("Enter the name of the existing data set: ")
    set = PdlmDataSet(nm)
    set.openFrom()

def addOrSave():
    global set
    global passAddOrSave
    while True:
        try:
            opt = input("Choose the following options: \n1 - Add new data \n21 - Plot current data set with l vs T \n22 - Plot current data set with sqrt(l) vs T \n23 - Plot current data set with sqrt(l) vs T w/ linear fit\n3 - Save the data set \n0 - Exit the program \nYour choice: ")
            if opt == "1":
                set.add()
            elif opt == "21":
                set.plot(1)
            elif opt == "22":
                set.plot(2)
            elif opt == "23":
                set.plot(3)
            elif opt == "3":
                set.save()
            elif opt == "0":
                while True:
                    try:
                        opt2 = input(
                            "Unsaved data will be losted. Are you sure to continue? (y/n) ")
                        if opt2 == "y":
                            passAddOrSave = True
                        elif opt2 == "n":
                            pass
                        else:
                            raise Exception(1)
                        break
                    except Exception:
                        print("Invalid choice. Please try again.")
            else:
                raise Exception(1)
            break
        except Exception:
            print("Invalid choice. Please try again.")
        else:
            print("Unknown error.")


passAddOrSave = False

set = PdlmDataSet()

initiate()

while passAddOrSave != True:
    addOrSave()

print("Session ended.")