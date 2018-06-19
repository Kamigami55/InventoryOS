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


class ModeType(Enum):
    BORROW = 1
    RETURN = 2



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

        # Button: take snapshot
        btn = tki.Button(self.root, text="Snapshot!",
            command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
            pady=10)

        # Button: mode
        self.modetext = tki.StringVar()
        self.modetext.set("BORROW Mode")
        btn = tki.Button(self.root, textvariable=self.modetext,
            command=self.changeMode)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
            pady=10)

        # Text: recognition result
        self.result = tki.StringVar()
        self.result.set("Recognition result")
        l = tki.Label(self.root, textvariable=self.result, width=15, height=2)
        l.pack(side='bottom', padx=10, pady=10, expand='yes')

        # Text: current user
        self.currentUser = tki.StringVar()
        self.currentUser.set("Current user")
        l = tki.Label(self.root, textvariable=self.currentUser, width=15, height=2)
        l.pack(side='bottom', padx=10, pady=10, expand='yes')

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
            self.mode = ModeType.RETURN
            self.modetext.set("RETURN Mode")
            print("Mode changed to RETURN")
        else:
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

                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

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

        # Print results
        print('Labels:')
        for label in labels:
            print(label.description)

        # Set result text
        if labels is None:
            self.result.set("Can't recognize")
        else:
            self.result.set(labels[0].description)


    def onClose(self):
        print("[INFO] close button pressed")
        self.cleanup()


    def cleanup(self):
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
        print("tkinter window successfully cleaned up")
