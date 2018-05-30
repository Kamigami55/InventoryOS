# -*- coding: utf-8 -*-
#!/usr/bin/python

'''
InventoryOS camera main.py
==============

Main script of InventoryOS camera component

'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from enum import Enum
 
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
        CameraApp().run()
    except KeyboardInterrupt:
        print("Exit")
        exit(0)
