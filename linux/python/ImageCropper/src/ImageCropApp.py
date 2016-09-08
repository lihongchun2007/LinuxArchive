#!/usr/bin/env python2

from kivy.app import App
from ImageCropWidget import ImageCropWidget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import  FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from os.path import expanduser
import os, glob

Builder.load_file('./ui.kv')
class ImageCropUI(BoxLayout):
    editImgDir = ObjectProperty()
    spinnerClassName = ObjectProperty()
    labelClassID = ObjectProperty()
    imageWidget = ObjectProperty()
    labelImageName = ObjectProperty()

    cropBoxClass = {'Car':1, 'Bus': 2, 'Taxi': 3}  #{class_name: class_id} 
    supportImageFormatList = ['jpg', 'png', 'jpeg', 'JPG', 'PNG']
    imageList = []
    currentImageIdx = 0
    outputPath = '/tmp'

    def __init__(self, **kwargs):
        super(ImageCropUI, self).__init__(**kwargs)
        self._load_class_name()
        self.spinnerClassName.bind(text=self.on_select_class_name)


    def _load_class_name(self):
        classNames = tuple(self.cropBoxClass.keys())
        self.spinnerClassName.text = 'Car'   #Default class name
        self.labelClassID.text = '1'
        self.spinnerClassName.values = classNames

        strClassID = str(self.cropBoxClass[self.spinnerClassName.text])
        self.imageWidget.setBoxClass(self.spinnerClassName.text, strClassID)

    def on_select_class_name(self, spinner, text):
        strClassID = str(self.cropBoxClass[text])
        self.labelClassID.text = strClassID

        self.imageWidget.setBoxClass(text, strClassID)

    def select_image_dir(self):
        startPath = self.editImgDir.text
        if startPath == '':
            startPath = expanduser('~')
        fileChooser = ImageDirDialog(path=startPath, \
                                     on_cancel=self.on_imgDirDialog_cancel, \
                                     on_ok=self.on_imgDirDialog_ok)
        self._popup = Popup(title="Select file", content=fileChooser, size_hint=(0.9, 0.9))
        self._popup.open()

    def on_imgDirDialog_cancel(self):
        self._popup.dismiss()

    def on_imgDirDialog_ok(self, path, select):
        if path != '':
            self.editImgDir.text = path
            self.outputPath = path + '/crops'

            if not os.path.exists(self.outputPath):
                os.makedirs(self.outputPath)

            self.updateImageList()
            if len(select) > 0 and select[0] in self.imageList:
                self.currentImageIdx = self.imageList.index(select[0])
            else:
                self.currentImageIdx = 0

            if len(self.imageList) > 0:
                self.imageWidget.save_crops_xml(self.outputPath)
                self.imageWidget.clear_image()
                self.imageWidget.source = self.imageList[self.currentImageIdx]
                self.labelImageName.text = self.imageList[self.currentImageIdx]

        self._popup.dismiss()

    def on_button_next(self):
        if len(self.imageList) == 0:
            return 
        #TODO
        #Save image crop information

        #Next image
        self.imageWidget.save_crops_xml(self.outputPath)
        self.imageWidget.clear_image()
        self.currentImageIdx = (self.currentImageIdx + 1)%len(self.imageList)

        self.imageWidget.source = self.imageList[self.currentImageIdx]
        self.labelImageName.text = self.imageList[self.currentImageIdx]

    def on_button_previous(self):
        if len(self.imageList) == 0:
            return
        #TODO
        #Load image crop information

        #Previous image
        self.imageWidget.save_crops_xml(self.outputPath)
        self.imageWidget.clear_image()
        self.currentImageIdx = (self.currentImageIdx - 1 \
                                + len(self.imageList))%len(self.imageList)
        self.imageWidget.source = self.imageList[self.currentImageIdx]
        self.labelImageName.text = self.imageList[self.currentImageIdx]

    def updateImageList(self):
        imgDir = self.editImgDir.text

        self.imageList = []
        for imgFormat in self.supportImageFormatList:
            imgFullDir = imgDir + '/*.' + imgFormat
            self.imageList = self.imageList + glob.glob(imgFullDir)

        self.imageList.sort()
        return self.imageList

class ImageDirDialog(FloatLayout):
    on_cancel = ObjectProperty()
    on_ok = ObjectProperty()
    path = ObjectProperty()

class ImageCropApp(App):
    def __init__(self, **kwargs):
        super(ImageCropApp,self).__init__(**kwargs)

    def build(self):
        return ImageCropUI()

if __name__ == '__main__':
    Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
    ImageCropApp().run()
