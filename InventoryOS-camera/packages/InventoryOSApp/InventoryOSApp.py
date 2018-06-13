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


class InventoryOSApp:
    def __init__(self, vs1, vs2, vs3, vs4):
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        self.vs1 = vs1
        self.vs2 = vs2
        self.vs3 = vs3
        # self.vs4 = vs4
        self.frame1 = None
        self.frame2 = None
        self.frame3 = None
        # self.frame4 = None
        self.thread = None
        self.stopEvent = None

        # initialize the root window and image panel
        self.root = tki.Tk()
        self.panel1 = None
        self.panel2 = None
        self.panel3 = None
        # self.panel4 = None

        # create a button, that when pressed, will take the current
        # frame and save it to file
        btn = tki.Button(self.root, text="Snapshot!",
            command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
            pady=10)

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



    def videoLoop(self):
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame1 = self.vs1.read()
                self.frame1 = imutils.resize(self.frame1, width=300)
                self.frame2 = self.vs2.read()
                self.frame2 = imutils.resize(self.frame2, width=300)
                self.frame3 = self.vs3.read()
                self.frame3 = imutils.resize(self.frame3, width=300)
                # self.frame4 = self.vs4.read()
                # self.frame4 = imutils.resize(self.frame4, width=300)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image1 = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
                image1 = Image.fromarray(image1)
                image1 = ImageTk.PhotoImage(image1)
                self.image1 = image1
                image2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
                image2 = Image.fromarray(image2)
                image2 = ImageTk.PhotoImage(image2)
                image3 = cv2.cvtColor(self.frame3, cv2.COLOR_BGR2RGB)
                image3 = Image.fromarray(image3)
                image3 = ImageTk.PhotoImage(image3)
                # image4 = cv2.cvtColor(self.frame4, cv2.COLOR_BGR2RGB)
                # image4 = Image.fromarray(image4)
                # image4 = ImageTk.PhotoImage(image4)

                if self.panel1 is None:
                    self.panel1 = tki.Label(image=image1)
                    self.panel1.image = image1
                    self.panel1.pack(side="left", padx=10, pady=10)
                else:
                    self.panel1.configure(image=image1)
                    self.panel1.image = image1

                if self.panel2 is None:
                    self.panel2 = tki.Label(image=image2)
                    self.panel2.image = image2
                    self.panel2.pack(side="left", padx=10, pady=10)
                else:
                    self.panel2.configure(image=image2)
                    self.panel2.image = image2

                if self.panel3 is None:
                    self.panel3 = tki.Label(image=image3)
                    self.panel3.image = image3
                    self.panel3.pack(side="left", padx=10, pady=10)
                else:
                    self.panel3.configure(image=image3)
                    self.panel3.image = image3

                # if self.panel4 is None:
                    # self.panel4 = tki.Label(image=image4)
                    # self.panel4.image = image4
                    # self.panel4.pack(side="left", padx=10, pady=10)
                # else:
                    # self.panel4.configure(image=image4)
                    # self.panel4.image = image4

        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self):
        # grab the current timestamp and use it to construct the
        # output path

        print("[INFO] Take snapshot pressed")
        # save the file
        print("[INFO] file saved")
        cv2.imwrite("image.jpg", self.frame3.copy())
        # print("[INFO] saved {}".format(filename))
        # image = types.Image(content=self.frame1.copy())

        with io.open("image.jpg", 'rb') as image_file:
            content = image_file.read()

        print("[INFO] file loaded")
        image = types.Image(content=content)

        response = self.visionClient.label_detection(image=image)
        labels = response.label_annotations

        # optionLayout = Window.get_parent_window().children[0].ids.optionlayout
        # optionLayout.ids.option1.text = labels[0].description
        # optionLayout.ids.option2.text = labels[1].description
        # optionLayout.ids.option3.text = labels[2].description

        print('Labels:')
        for label in labels:
            print(label.description)


    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs1.stop()
        self.vs2.stop()
        self.vs3.stop()
        # self.vs4.stop()
        self.root.quit()
