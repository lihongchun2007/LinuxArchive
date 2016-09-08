#!/usr/bin/env python2

from kivy.config import Config
from ImageCropApp import ImageCropApp

if __name__ == '__main__':
    Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
    ImageCropApp().run()
