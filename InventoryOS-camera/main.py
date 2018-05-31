#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
InventoryOS camera main.py
==============

Main script of InventoryOS camera component

Before run this script, you should set credential
set environment variable $GOOGLE_APPLICATION_CREDENTIALS
to the path of your credential.json downloaded from
google cloud
'''


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from enum import Enum


import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'captured.png')


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
    '/home/eason/projects/InventoryOS/\
InventoryOS-camera/google-vision-credential.json'


class ModeType(Enum):
    BORROW = 1
    RETURN = 2


class CameraLayout(BoxLayout):

    mode = ModeType.BORROW

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        camera.export_to_png("captured.png")
        print("Captured")

        # Start performing object detection using Google Vision API
        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = visionClient.label_detection(image=image)
        labels = response.label_annotations

        print('Labels:')
        for label in labels:
            print(label.description)

    def switchMode(self):
        '''
        Switch camera operation mode between Borrow and Return
        '''
        mode_switch = self.ids['mode_switch']
        if self.mode == ModeType.BORROW:
            mode_switch.text = "Return mode"
            self.mode = ModeType.RETURN
        else:
            mode_switch.text = "Borrow mode"
            self.mode = ModeType.BORROW

        print("Mode switched to %s" % self.mode.name)


class CameraApp(App):

    def build(self):
        return CameraLayout()


if __name__ == '__main__':
    try:
        # Instantiates a client for google vision API
        visionClient = vision.ImageAnnotatorClient()

        CameraApp().run()
    except KeyboardInterrupt:
        print("Exit")
        exit(0)
