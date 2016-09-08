#!/usr/bin/env python2

from kivy.uix.image import *
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Line, InstructionGroup
from kivy.lang import Builder
from kivy.uix.bubble import Bubble
from kivy.uix.label import Label

from xml.etree.ElementTree import Element, SubElement, tostring, Comment

import os, cv2

class ImageCropWidget(Image):
    def __init__(self, **kwargs):
        super(ImageCropWidget, self).__init__(**kwargs)

        self.menu = PopMenu(self)
        self.selectBoxs = None    # (box, boxBorder, boxClassName, boxClassID)
        self.selectBoxShadow = None

        #About cropbox
        self.boxList = []  # [(newBox, newBoxBorder, boxClassName, boxClassID)]
        self.newBox = None
        self.newBoxBorder = None
        self.newBoxStartPoint = None

        self.boxClass = None

    def setBoxClass(self, boxClassName, boxClassID):
        self.boxClass = [boxClassName, boxClassID]

    def clear_image(self):
        for boxs in self.boxList:
            self.canvas.remove(boxs[0])
            self.canvas.remove(boxs[1])
    
        if self.selectBoxShadow != None:
            self.canvas.remove(self.selectBoxShadow)

        self.boxList = []
        self.newBox = None
        self.newBoxBorder = None
        self.newBoxStartPoint = None

        self.selectBoxs = None    # (box, boxBorder)
        self.selectBoxShadow = None

    def save_crops(self, dirName):
        
        if self.source != None:
            orignalImagePath = os.path.dirname(self.source)
            originalImageName = os.path.basename(self.source).split('.')[0]

            if len(self.boxList) > 0:
                logFile = open(dirName + '/' + originalImageName + '.txt', 'w')

            for idx, box in enumerate(self.boxList):
                imgBox, imgBoxBorder, boxClassName, boxClassID = box
                fileName = dirName + '/' + boxClassName + '-' + originalImageName + '-' + str(idx) + '.jpg'
                x, y, w, h = self.save_crop_box(imgBox, fileName)

                logFile.write(os.path.basename(self.source) + ' ' \
                                        + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n')

    def save_crops_xml(self, dirName):
        if self.source != None:
            orignalImagePath = os.path.dirname(self.source)
            originalImageName = os.path.basename(self.source).split('.')[0]

            if len(self.boxList) > 0:
                logFile = open(dirName + '/' + originalImageName + '.xml', 'w')
            else:
                return

            ## Ready to write xml
            top = Element('annotation')
            folder = SubElement(top, 'folder')
            folder.text = orignalImagePath
            imageName = SubElement(top, 'image_name')
            imageName.text = os.path.basename(originalImageName)

            for idx, box in enumerate(self.boxList):
                imgBox, imgBoxBorder, boxClassName, boxClassID = box
                fileName = dirName + '/' + boxClassName + '-' + originalImageName + '-' + str(idx) + '.jpg'
                x, y, w, h = self.save_crop_box(imgBox, fileName)

                obj = SubElement(top, 'object')
                cls = SubElement(obj, 'class')
                cls.text = boxClassName
                boundBox = SubElement(obj, 'bndbox')
                xmin = SubElement(boundBox, 'xmin')
                xmin.text = str(x)
                xmax = SubElement(boundBox, 'xmax')
                xmax.text = str(x + w)
                ymin = SubElement(boundBox, 'ymin')
                ymin.text = str(y)
                ymax = SubElement(boundBox, 'ymax')
                ymax.text = str(y + h)

            logFile.write(tostring(top))
            logFile.close()

    def on_mouse_left_down(self, touch):
        print 'touch point:', touch.pos, 'image pos:', self.image_pos(), 'image size:', self.norm_image_size
        with self.canvas:
            Color(1, 0, 0, .2)
            self.newBoxStartPoint = (touch.x, touch.y)
            self.newBox = Rectangle(pos=self.newBoxStartPoint, size=(0, 0))
            Color(1, 0, 0)
            self.newBoxBorder = Line(rectangle=(touch.x, touch.y, 0, 0), width=2)

        self.startPos=(touch.x, touch.y)

        return True

    def on_mouse_left_move(self, touch):
        if self.newBox != None:
            newBoxSize = (touch.x - self.newBoxStartPoint[0], touch.y - self.newBoxStartPoint[1])
            self.newBox.pos = self.newBoxStartPoint
            self.newBox.size = newBoxSize
            self.newBoxBorder.rectangle=(self.newBoxStartPoint[0], self.newBoxStartPoint[1], newBoxSize[0], newBoxSize[1])

        return True

    def on_mouse_left_up(self, touch):
        if self.newBox != None :
            #Remove new box if it is small
            if abs(self.newBox.size[0]) > 10 and abs(self.newBox.size[1]) > 10:
                self.boxList.append((self.newBox, self.newBoxBorder, self.boxClass[0], self.boxClass[1]))
                center = (self.newBox.pos[0] + self.newBox.size[0]/2, self.newBox.pos[1] + self.newBox.size[1]/2)
                #with self.canvas:
                #    Label(text=self.boxClass[0], pos=center, width='40sp', height='10sp')
            else:
                print 'Remove new box'
                self.canvas.remove(self.newBox)
                self.canvas.remove(self.newBoxBorder)
                
        self.newBox = None
        self.newBoxBorder = None

        return True

    def on_mouse_right_down(self, touch):
        pass

    def on_mouse_right_up(self, touch):
        print self.boxList
        self.show_menu(touch.pos)
        return False

    def on_touch_down(self, touch):
        if not self.in_image(touch.pos):
            return False
        if self.source == None:
            return False

        if not self.menu_visible():
            if 'button' in touch.profile:
                if touch.button == 'left':
                    self.on_mouse_left_down(touch)
                elif touch.button == 'right':
                    self.on_mouse_right_down(touch)

        return super(ImageCropWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.in_image(touch.pos):
            return False
        if self.source == None:
            return False

        if not self.menu_visible():
            if 'button' in touch.profile:
                if touch.button == 'left':
                    self.on_mouse_left_move(touch)
               
        return super(ImageCropWidget, self).on_touch_move(touch)
    
    def on_touch_up(self,  touch):
        if not self.in_image(touch.pos):
            self.on_mouse_left_up(touch)
            return False

        if self.source == None:
            return False

        if self.menu_visible() and self.menu.in_menu(touch.pos):
            return super(ImageCropWidget, self).on_touch_up(touch)

        if self.menu_visible():
            self.hide_menu()
        else:
            if 'button' in touch.profile:
                if touch.button == 'left':
                    self.on_mouse_left_up(touch)
                elif touch.button == 'right':
                    self.on_mouse_right_up(touch)
    
        return super(ImageCropWidget, self).on_touch_up(touch)

    def show_menu(self, pos):
        if self.get_select_box(pos):
            if self.menu not in self.children:
                self.show_select_box()
                self.add_widget(self.menu)
                self.menu.pos = (pos[0] - self.menu.size[0]/2, pos[1])
            else:
                self.remove_widget(self.menu)

    def hide_menu(self):
        if self.menu in self.children:
            self.remove_widget(self.menu)

        self.clear_select_box()

    def menu_visible(self):
        if self.menu in self.children:
            return True
        return False

    def get_image_scale(self):
        normImageSize = self.norm_image_size
        realImageSize = self.original_image_size()
        return (float(realImageSize[0])/normImageSize[0], float(realImageSize[1])/normImageSize[1])

    #TODO
    def get_crop_boxes(self):
        return [self.image_box_2_crop_box(box[0], self.get_image_scale()) for box in self.boxList]


    def image_box_2_crop_box(self, imgBox, scale):
        image_pos = self.image_pos()
        image_size = self.norm_image_size

        print imgBox.pos, imgBox.size

        image_left_right_cornor = (image_pos[0], image_pos[1] + image_size[1])
        
        x0 = imgBox.pos[0]
        y0 = imgBox.pos[1]
        if imgBox.size[0] < 0:
            x0 = x0 + imgBox.size[0]
        if imgBox.size[1] > 0:
            y0 = y0 + imgBox.size[1]

        x = x0 - image_left_right_cornor[0] 
        y = image_left_right_cornor[1] - y0

        return (int(x*scale[0]), int(y*scale[1]), 
                int(abs(imgBox.size[0])*scale[0]), int(abs(imgBox.size[1])*scale[1]))

    def save_crop_box(self, imgBox, imageName, logFile = None):
        x, y, w, h= self.image_box_2_crop_box(imgBox, self.get_image_scale())

        im = cv2.imread(self.source)
        box_image = im[y:y+h, x:x+w]
        cv2.imwrite(imageName, box_image)

        return x, y, w, h
    
    def get_select_box(self, pos):
        for box in self.boxList:
            startPoint = box[0].pos
            endPoint = (box[0].pos[0] + box[0].size[0], box[0].pos[1] + box[0].size[1])

            if between(pos[0], startPoint[0], endPoint[0]) \
                and between(pos[1], startPoint[1], endPoint[1]):
                    self.selectBoxs = box 
                    return True
        return False

    def show_select_box(self):
        if self.selectBoxs == None:
            return

        if self.selectBoxShadow != None:
            self.canvas.remove(self.selectBoxShadow)
            self.selectBoxShadow = None

        with self.canvas:
            Color(0, 1, 0, 1)
            #self.selectBoxShadow = Rectangle(pos=self.selectBoxs[0].pos, size=self.selectBoxs[0].size)
            rect = (self.selectBoxs[0].pos[0], self.selectBoxs[0].pos[1], \
                    self.selectBoxs[0].size[0], self.selectBoxs[0].size[1])

            self.selectBoxShadow = Line(rectangle=rect, width=2)

    def clear_select_box(self):
        if self.selectBoxShadow != None:
            self.canvas.remove(self.selectBoxShadow)
            self.selectBoxShadow = None

        self.selectBoxs = None

    def in_select_mode(self):
        if self.selectBoxs != None and self.selectBoxShadow != None:
            return True
        return False

    def remove_select_box(self):
        print self.selectBoxs
        print self.selectBoxShadow

        if self.in_select_mode():
            self.canvas.remove(self.selectBoxs[0])
            self.canvas.remove(self.selectBoxs[1])
            self.canvas.remove(self.selectBoxShadow)

            self.boxList.remove(self.selectBoxs)

            print 'delete select box'
        self.selectBoxs = None
        self.selectBoxShadow = None

    def image_pos(self):
        widgetPos = self.pos
        widgetSize = self.size
        imageSize = self.norm_image_size

        x = self.pos[0] + (self.size[0] - self.norm_image_size[0])/2.
        y = self.pos[1] + (self.size[1] - self.norm_image_size[1])/2.

        return (x, y)
    
    def original_image_size(self):
        return self.__dict__['_coreimage'].size

    def in_image(self, pos):
        startPoint = self.image_pos()
        endPoint = (startPoint[0] + self.norm_image_size[0], startPoint[1] + self.norm_image_size[1])

        if between(pos[0], startPoint[0], endPoint[0]) \
                and between(pos[1], startPoint[1], endPoint[1]):
            return True
        
        return False

## Context Menu
Builder.load_string('''
<PopMenu>
    size_hint: (None, None)
    size: (60, 60)
    pos_hint: {'center_x': .5, 'y': .6}
    BubbleButton:
        text: 'Delete'
        on_release: root.on_menu_delete()
    #BubbleButton:
    #    text: 'Move'
    #    on_release: root.on_menu_move()
    #BubbleButton:
    #    text: 'Resize'
    #    on_release: root.on_menu_resize()
''')

class PopMenu(Bubble):
    def __init__(self, parentWidget, **kwargs):
        super(PopMenu, self).__init__(**kwargs)

        self.parentWidget = parentWidget

    def on_menu_delete(self):
        #print self.parentWidget.get_crop_boxes()
        print 'Delete select box'
        self.parentWidget.remove_select_box()
        self.parentWidget.hide_menu()

    def on_menu_resize(self):
        print 'Resize is clicked'

    def on_menu_move(self):
        print 'Move is clicked'

    def in_menu(self, pos):
        startPoint = self.pos
        endPoint = (self.pos[0] + self.size[0], self.pos[1] + self.size[0])

        if between(pos[0], startPoint[0], endPoint[0]) \
                and between(pos[1], startPoint[1], endPoint[1]):
            return True

        return False

def between(x, x1, x2):
    if x >= x1 and x <= x2:
        return True
    elif x >= x2 and x <= x1:
        return True
    return False
