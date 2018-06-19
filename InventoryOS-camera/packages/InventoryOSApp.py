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
        self.imagePanel.grid(row=0, column=0)

        # Buttons frame
        self.buttonFrame = tki.Frame(self.root)
        self.buttonFrame.grid(row=1, column=0)

        # Button: take snapshot
        btn = tki.Button(self.buttonFrame, text="Recognize!",
            command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
            pady=10)

        # Button: mode
        self.modetext = tki.StringVar()
        self.modetext.set("BORROW Mode")
        btn = tki.Button(self.buttonFrame, textvariable=self.modetext,
            command=self.changeMode, bg="yellow")
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
                 pady=10)

        # Texts frame
        self.textFrame = tki.Frame(self.root)
        self.textFrame.grid(row=0, column=1, rowspan=2, sticky='N')

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
        l = tki.Label(srFrame, textvariable=self.serverResult, fg='blue', width=30, wraplength=250, height=6, justify='left', anchor='nw')
        l.pack()

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


    def changeMode(self):
        if self.mode == ModeType.BORROW:
            # change from BORROW to RETURN
            self.mode = ModeType.RETURN
            self.modetext.set("RETURN Mode")
            print("Mode changed to RETURN")
        elif self.mode == ModeType.RETURN:
            # change from RETURN to ADDNEW
            self.mode = ModeType.ADDNEW
            self.modetext.set("ADDNEW Mode")
            print("Mode changed to ADDNEW")
        else:
            # change from ADDNEW to BORROW
            self.mode = ModeType.BORROW
            self.modetext.set("BORROW Mode")
            print("Mode changed to BORROW")


    def videoLoop(self):
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            while not self.stopEvent.is_set():

                user = self.RFIDReader.read()
                if user is not None:
                    self.currentUser.set(user)

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
                # if self.panel is None:
                    # self.panel = tki.Label(image=image)
                    # self.panel.image = image
                    # self.panel.pack(side="left", padx=10, pady=10)
                # else:
                    # self.panel.configure(image=image)
                    # self.panel.image = image

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


    def onClose(self):
        print("[INFO] close button pressed")
        self.cleanup()


    def cleanup(self):
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
        print("tkinter window successfully cleaned up")
