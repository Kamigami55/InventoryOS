from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import Tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
import io
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from .myRFID import RFIDReader
from enum import Enum
import requests


class ModeType(Enum):
    BORROW = 'BORROW'
    RETURN = 'RETURN'
    ADDNEW = 'ADDNEW'



class InventoryOSApp:
    def __init__(self, vs):
        self.vs = vs
        self.frame = None
        self.thread = None
        self.root = tki.Tk()
        self.panel = None
        self.stopEvent = None
        self.RFIDReader = RFIDReader()
        self.mode = ModeType.BORROW


        # Tkinter UI organize

        # Image panel
        self.image = ImageTk.PhotoImage(Image.open("image.jpg"))
        self.imagePanel = tki.Label(image=self.image)
        self.imagePanel.image = self.image
        self.imagePanel.pack(side='left')

        # right frame
        rframe = tki.Frame(self.root)
        rframe.pack(side='left')

        # Texts frame
        self.textFrame = tki.Frame(rframe)
        self.textFrame.pack()

        # Text: recognition result
        rrFrame = tki.Frame(self.textFrame)
        rrFrame.pack(fill='x')
        self.result = tki.StringVar()
        self.result.set("None")
        l = tki.Label(rrFrame, text="Recognition Result: ", justify='left')
        l.pack(side='left')
        l = tki.Label(rrFrame, textvariable=self.result, fg='green', justify='left', pady=5)
        l.pack(side='left')

        # Text: current user
        cuFrame = tki.Frame(self.textFrame)
        cuFrame.pack(fill='x')
        self.currentUser = tki.StringVar()
        self.currentUser.set("None")
        l = tki.Label(cuFrame, text="Current User: ", justify='left')
        l.pack(side='left')
        l = tki.Label(cuFrame, textvariable=self.currentUser, fg='red', justify='left', pady=5)
        l.pack(side='left')

        # Text: server response
        srFrame = tki.Frame(self.textFrame)
        srFrame.pack(fill='x')
        self.serverResult = tki.StringVar()
        self.serverResult.set("None")
        l = tki.Label(srFrame, text="Server Response: ", justify='left', anchor='nw')
        l.pack(fill='x')
        l = tki.Label(srFrame, textvariable=self.serverResult, fg='blue', width=30, wraplength=230, height=6, justify='left', anchor='nw')
        l.pack()

        # Buttons frame
        self.buttonFrame = tki.Frame(rframe)
        self.buttonFrame.pack(side='bottom', fill='x')

        # mode buttons frame
        mbFrame = tki.Frame(self.buttonFrame)
        mbFrame.pack(fill='x')

        self.borrowbtn = tki.Button(mbFrame, text="BORROW", bg='cyan', command= lambda: self.changeMode(ModeType.BORROW))
        self.borrowbtn.pack(side="left", fill="x")
        self.returnbtn = tki.Button(mbFrame, text="RETURN", bg='white', command= lambda: self.changeMode(ModeType.RETURN))
        self.returnbtn.pack(side="left", fill="x")
        self.addnewbtn = tki.Button(mbFrame, text="ADDNEW", bg='white', command= lambda: self.changeMode(ModeType.ADDNEW))
        self.addnewbtn.pack(side="left", fill="x")

        # Button: take snapshot
        self.recogbtn = tki.Button(self.buttonFrame, text="Recognize!", bg='green', command=self.takeSnapshot, state='disabled')
        self.recogbtn.pack(fill="x")


        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("InventoryOS")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        # Instantiates a client for google vision API
        self.visionClient = vision.ImageAnnotatorClient()


    def changeMode(self, mode):
        self.mode = mode
        self.borrowbtn.config(bg='white')
        self.returnbtn.config(bg='white')
        self.addnewbtn.config(bg='white')
        if mode == ModeType.BORROW:
            self.borrowbtn.config(bg='cyan')
            print("Mode changed to BORROW")
        elif mode == ModeType.RETURN:
            self.returnbtn.config(bg='yellow')
            print("Mode changed to RETURN")
        else:
            self.addnewbtn.config(bg='magenta')
            print("Mode changed to ADDNEW")


    def videoLoop(self):
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            while not self.stopEvent.is_set():

                # Deal with RDIF stuff
                user = self.RFIDReader.read()
                if user is not None:
                    self.currentUser.set(user)
                    self.recogbtn.config(state='normal')

                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)
                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                self.image = image

                self.imagePanel.configure(image=image)
                self.imagePanel.image = image

        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self):
        print("[INFO] Take snapshot pressed")

        # save image as file
        cv2.imwrite("image.jpg", self.frame.copy())
        print("[INFO] image saved")

        # load image from file HACK
        with io.open("image.jpg", 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        print("[INFO] image loaded")

        # Recogonize by GoogleVisionAPI
        response = self.visionClient.label_detection(image=image)
        labels = response.label_annotations


        # Set result text
        if labels is None:
            self.result.set("Can't recognize")
        else:
            # Print results
            print('Labels:')
            for label in labels:
                print(label.description)

            result = labels[0].description
            self.result.set(result)

            username = self.currentUser.get()
            if username == "None":
                print("User name not set, abort")
            else:
                print("POST data to server")
                # Send request to server
                data = {
                    'username' : username,
                    'mode': self.mode.value,
                    'item_name': result
                }
                # headers = {'Content-type': 'multipart/form-data'}
                # files = {'media': io.open('image.jpg', 'rb')}
                url = 'http://makereallabs.com:3000/device/api'
                r = requests.post(url, data=data)
                print(r.text)
                self.serverResult.set(r.text)


                if self.mode == ModeType.ADDNEW:
                    files = {'item_image': io.open('image.jpg', 'rb')}
                    url = 'http://makereallabs.com:3000/device/image'
                    r = requests.post(url, files=files)
                    print(r.text)
                    self.serverResult.set(self.serverResult.get() + "\n" + r.text)


    def onClose(self):
        print("[INFO] close button pressed")
        self.cleanup()


    def cleanup(self):
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
        print("tkinter window successfully cleaned up")
