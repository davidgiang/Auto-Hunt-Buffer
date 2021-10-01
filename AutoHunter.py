import pyautogui
import time
import tkinter as tk
from tkinter import *
import threading
from threading import *
import os

class AutoHunter():

    file_format = '.png'
    stop_bool = False

    def __init__(self, num_runs, buy, confirm, stageclear, start, tryagain):
        self.num_runs = num_runs
        self.buy = buy
        self.confirm = confirm
        self.stageclear = stageclear
        self.start = start
        self.tryagain = tryagain
        self.timers_arr = []

        with open('timers.txt', 'r') as f:
            for line in f:
                word = ""
                for char in line:
                    if char != " ":
                        word += char
                    else:
                        break
                self.timers_arr.append(word)
            print(self.timers_arr)

    def startAH(self):
        self.stop_bool = False
        runs_to_do = self.num_runs

        while runs_to_do > 0:
            if self.stop_bool == True:
                num_runs.set("Stopped")
                break

            runs_to_do -= 1

            self.findAndClickButton('start')
            time.sleep(float(self.timers_arr[0])) # after clicking start
            self.findAndClickButton('buy')
            time.sleep(float(self.timers_arr[1])) # after clicking buy
            self.findAndClickButton('start')
            time.sleep(float(self.timers_arr[2])) # check again for start button in case bought leif
            self.waitUntilClear()
            time.sleep(float(self.timers_arr[3])) # after clicking stage clear
            self.findAndClickButton('confirm')
            time.sleep(float(self.timers_arr[4])) # after clicking confirm
            self.findAndClickButton('tryagain')
            time.sleep(float(self.timers_arr[5])) # after clicking try again

            num_runs.set(runs_to_do)

    def stopAH(self):
        print("Setting stop bool to true")
        self.stop_bool = True

    def findAndClickButton(self, image):
        image_ff = image + self.file_format
        print("Finding " + str(image))
        image_box = pyautogui.locateOnScreen(image_ff, confidence = 0.9, grayscale=True)

        if image_box == None:
            print(str(image) + " not found")
            return

        pyautogui.moveTo(image_box)
        pyautogui.click(button='left')
        print("Clicked " + str(image) + " button")

    def waitUntilClear(self):
        print("Waiting to clear stage")
        image_box = pyautogui.locateOnScreen("stageclear.png", confidence = 0.9, grayscale=True)

        while image_box == None:
            if self.stop_bool == True:
                return
            image_box = pyautogui.locateOnScreen("stageclear.png", confidence=0.9, grayscale=True)
            print("Stage clear not found")
            time.sleep(float(1))

        pyautogui.moveTo(image_box)
        pyautogui.click(button='left')
        print("Clicked stage clear button")

root = tk.Tk()

num_runs = StringVar()
num_runs.set('Not entered')

def bootUp():
    try:
        global AH
        AH = AutoHunter(int(num_runs.get()), "buy.png", "confirm.png", "stageclear.png", "start.png", "tryagain.png")
        print("AH initiated")
    except:
        print("Failed to initiate AH")

def enterNumRuns():
    print("Submitting Num Runs")
    get_call = numRunEntry.get()
    try:
        if isinstance(int(get_call), int):
            num_runs.set(get_call)
        else:
            num_runs.set("Invalid")
    except:
        num_runs.set("Invalid")

    bootUp()

def startButton():
    print("Starting Auto Hunter")
    startButton['state'] = 'disabled'
    numRunSubmit['state'] = 'disabled'

    if num_runs.get() == 'Invalid' or num_runs.get() == 'Not entered':
        print('Error')
    else:
        try:
            threading.Thread(target=AH.startAH).start()
        except:
            print("No AH initiated yet")

def stopButton():
    print("Stopping Auto Hunter")
    startButton['state'] = 'normal'
    numRunSubmit['state'] = 'normal'

    try:
        threading.Thread(target=AH.stopAH).start()
    except:
        print("No AH initated yet")

########################################

startButtonFrame = tk.Frame(
    master = root,
    height = 500,
    width = 500
)

stopButtonFrame = tk.Frame(
    master = root,
    height = 500,
    width = 500
)

startButton = tk.Button(
    master = startButtonFrame,
    text = "Start",
    width = 5,
    height = 1,
    bg = "gray",
    fg = "black",
    command = startButton
)

stopButton = tk.Button(
    master = stopButtonFrame,
    text = "Stop",
    width = 5,
    height = 1,
    bg = "gray",
    fg = "black",
    command = stopButton
)

numRunFrame = tk.Frame(
    master = root,
    height = 500,
    width = 500
)

numRunLabel = tk.Label(
    master = numRunFrame,
    text = 'Enter Run Amount: '
)

numRunEntry = tk.Entry(
    master = numRunFrame,
    width = 17
)

numRunsToDo = tk.Label(
    master = root,
    text = "Runs Left to Do: "
)

numRunAmt = tk.Label(
    master = root,
    textvariable = num_runs
)

numRunSubmit = tk.Button(
    master=root,
    text="Enter",
    width=5,
    height=1,
    bg="gray",
    fg="black",
    command=enterNumRuns
)

####

startButtonFrame.pack()
startButtonFrame.place(relx=0.04, rely=0.85)

stopButtonFrame.pack()
stopButtonFrame.place(relx=0.22, rely=0.85)

startButton.pack()
stopButton.pack()

numRunFrame.pack()
numRunFrame.place(relx=0.04, rely=0.1)
numRunLabel.pack(side="left")
numRunEntry.pack()

numRunsToDo.pack()
numRunsToDo.place(relx=0.04, rely=0.48)
numRunAmt.pack()
numRunAmt.place(relx=0.45, rely=0.48)

numRunSubmit.pack()
numRunSubmit.place(relx=0.825, rely=0.085)

root.title("Auto Hunter by Traase")
root.geometry("320x240")
root.resizable(False, False)
root.mainloop()