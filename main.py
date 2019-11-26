#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Tkinter import *
import tkMessageBox, tkFileDialog
from PIL import Image, ImageTk
import ttk
import os
import glob
import random
import xml.etree.ElementTree as ET
import io
import convert

# colors for the bboxes
COLORS = ['red', 'blue', 'olive', 'teal', 'cyan', 'green', 'black']
# image sizes for the examples
SIZE = 256, 256

class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("Yolo Annotator")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width = FALSE, height = FALSE)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.xmlOutDir =''
        self.cur = 0
        self.total = 0
        self.category = ''
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None
        self.currentLabelclass = ''
        self.cla_can_temp = []
        self.classcandidate_filename = 'class.txt'
        self.classcnt = 0

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.hl = None
        self.vl = None

        # ----------------- GUI stuff ---------------------
        # dir entry & load
        #self.label = Label(self.frame, text = "Image Dir:")
        #self.label.grid(row = 0, column = 0, sticky = E)
        #self.entry = Entry(self.frame)
        #self.entry.grid(row = 0, column = 1, sticky = W+E)
        self.ldProjBtn = Button(self.frame, text = "Load Image", command = self.loadDir)
        self.ldProjBtn.grid(row = 0, column = 0,sticky = W+E, padx=5)
        #self.ldImgBtn = Button(self.frame, text = "Load XML", command = self.loadXML)
        #self.ldImgBtn.grid(row = 0, column = 1,sticky = W, padx=5)

        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.parent.bind("<Escape>", self.cancelBBox)  # press <Espace> to cancel current bbox
        self.parent.bind("s", self.cancelBBox)
        self.parent.bind("a", self.prevImage) # press 'a' to go backforward
        self.parent.bind("d", self.nextImage) # press 'd' to go forward
        self.parent.bind("r", self.clearBBoxShortcut)
        self.mainPanel.grid(row = 1, column = 1, columnspan = 3, rowspan = 4, sticky = W+N)

        # choose class
        self.classname = StringVar()
        self.classcandidate = ttk.Combobox(self.frame,state='readonly',textvariable=self.classname)
        self.classcandidate.grid(row=1,column=4)
        if os.path.exists(self.classcandidate_filename):
        	with open(self.classcandidate_filename) as cf:
        		for line in cf.readlines():
        			# print line
        			self.cla_can_temp.append(line.strip('\n'))
        			self.classcnt +=1

        self.classcandidate['values'] = self.cla_can_temp
        self.classcandidate.current(0)
        self.parent.bind('<Key>', self.setClassShortcut)
        #self.parent.bind("1", lambda e: self.setClassShortcut(0))
        #self.parent.bind("2", lambda e: self.setClassShortcut(1))
        #2self.parent.bind("3", lambda e: self.setClassShortcut(2))
        self.currentLabelclass = self.classcandidate.get() #init
        self.classcandidate.bind('<<ComboboxSelected>>', self.setClass)
        #self.btnclass = Button(self.frame, text = 'ComfirmClass', command = self.setClass)
        #self.btnclass.grid(row=2,column=2,sticky = W+E)

        # showing bbox info & delete bbox
        self.lb1 = Label(self.frame, text = 'Bounding boxes:')
        self.lb1.grid(row = 3, column = 4,  sticky = W+N)
        self.listbox = Listbox(self.frame, width = 22, height = 12)
        self.listbox.grid(row = 4, column = 4, sticky = N+S)
        self.btnDel = Button(self.frame, text = 'Clear', command = self.delBBox)
        self.btnDel.grid(row = 5, column = 4, sticky = W+E+N)
        self.btnClear = Button(self.frame, text = 'ClearAll', command = self.clearBBox)
        self.btnClear.grid(row = 6, column = 4, sticky = W+E+N)

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 7, column = 1, columnspan = 4, sticky = W+E)
        self.conv2YoloBtn = Button(self.ctrPanel, text='Convert YOLO', width = 15, command = self.convert2Yolo)
        self.conv2YoloBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.resetChkBtn = Button(self.ctrPanel, text='ResetCheckpoint', width = 15, command = self.resetCheckpoint)
        self.resetChkBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.loadChkBtn = Button(self.ctrPanel, text='LoadCheckpoint', width = 15, command = self.loadCheckpoint) 
        self.loadChkBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.skipBtn = Button(self.ctrPanel, text ='Skip', width = 10, command = self.skipImage)
        self.skipBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)


        # example pannel for illustration
        self.egPanel = Frame(self.frame, border = 10)
        self.egPanel.grid(row = 1, column = 0, rowspan = 5, sticky = N)
        self.tmpLabel2 = Label(self.egPanel, text = "Key Shortcut :\na : Prev\nd : Next\ns : Cancel\nr : Delete BB\n1-9 : Select Class")
        self.tmpLabel2.pack(side = TOP)
        self.tmpLabel3 = Label(self.egPanel, text = "\nBasic Usage :\n1.Load Image\n2.Annotate\n3.Convert Yolo")
        self.tmpLabel3.pack(side = TOP)
        self.egLabels = []
        for i in range(3):
            self.egLabels.append(Label(self.egPanel))
            self.egLabels[-1].pack(side = TOP)

        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side = RIGHT)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

        # for debugging
##        self.setImage()
##        self.loadDir()

    def loadDir(self, dbg = False):
        if not dbg:
            #s = self.entry.get()
            self.parent.focus()
            #self.category = int(s)
            s = str(tkFileDialog.askdirectory(initialdir=os.getcwd())).split('/')[-1]
            self.category = s
        else:
            s = r'D:\workspace\python\labelGUI'
##        if not os.path.isdir(s):
##            tkMessageBox.showerror("Error!", message = "The specified dir doesn't exist!")
##            return

         # get image list
        self.imageDir = os.path.join(r'./Images', '%s' %(self.category))
        #print self.imageDir 
        #print self.category
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.JPG'))
        #print self.imageList
        if len(self.imageList) == 0:
            tkMessageBox.showinfo("Error", "No .JPG images found in the specified dir!")
            print 'No .JPG images found in the specified dir!'
            return

        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)
        
         # set up output dir
        self.outDir = os.path.join(r'./Result', '%s' %(self.category))
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
        
        self.loadImage()
        print '%d images loaded from %s' %(self.total, self.category)
        tkMessageBox.showinfo("Info", "%d images loaded from %s" %(self.total, self.category))

    def loadImage(self):
        # load image
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(imagepath)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = max(self.tkimg.width(), 400), height = max(self.tkimg.height(), 400))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

        # load labels
        self.clearBBox()
        self.imagename = os.path.split(imagepath)[-1].split('.jpg')[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        bbox_cnt = 0
        
        self.loadBBox()
                    

    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            f.write('%d\n' %len(self.bboxList))
            for bbox in self.bboxList:
                f.write(' '.join(map(str, bbox)) + '\n')
        print 'Image No. %d saved' %(self.cur)


    def mouseClick(self, event):
        if self.STATE['click'] == 0:
            self.STATE['x'], self.STATE['y'] = event.x, event.y
        else:
            x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
            y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
            self.bboxList.append((x1, y1, x2, y2, self.currentLabelclass))
            self.bboxIdList.append(self.bboxId)
            self.bboxId = None
            self.listbox.insert(END, '%s : (%d, %d) -> (%d, %d)' %(self.currentLabelclass,x1, y1, x2, y2))
            self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
        self.STATE['click'] = 1 - self.STATE['click']

    def mouseMove(self, event):
        self.disp.config(text = 'x: %d, y: %d' %(event.x, event.y))
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
            self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], \
                                                            event.x, event.y, \
                                                            width = 2, \
                                                            outline = COLORS[len(self.bboxList) % len(COLORS)])

    def cancelBBox(self, event):
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
                self.bboxId = None
                self.STATE['click'] = 0

    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)

    def clearBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []
    
    def clearBBoxShortcut(self, event):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []
        
    '''def loadXML(self, event = None):
        if (self.category == ''):
            tkMessageBox.showinfo("Error", "Please Load Image first")
        else:
            basePath = "C:/DeepEye/Data/Result/request"
            xmlFiles = os.listdir(basePath)
            for xml in xmlFiles:
                if not(os.path.isfile(self.imageDir+'/'+xml.split('.xml.req')[0]+'_C.jpg')):
                    continue
                
                fullPath = os.path.join(basePath, xml)
                if os.path.isfile(fullPath):
                    f = io.open(fullPath,'r', encoding = 'euc-kr')
                    text = f.read().encode('utf-8')
                    f.close()
                    root = ET.fromstring(text)

                    for detect in root.findall('./Detections/detect'):
                        xmin = int(detect.find('rectx').text)
                        ymin = int(detect.find('recty').text)
                        xmax = int(detect.find('rectx').text) + int(detect.find('rectw').text)
                        ymax = int(detect.find('recty').text) + int(detect.find('recth').text)
                        classCode = detect.find('class').text
                        classLabel = ''
                        if (classCode == '0'):
                            classLabel = 'pothole'
                        elif (classCode == '1'):
                            classLabel = 'patchdamaged'
                        elif (classCode == '2'):
                            classLabel = 'spalling'
                        
                        saveName = xml.split('.xml.req')[0] + '_C.txt'
                        savePath = os.path.join(self.outDir, saveName)
                        with open(savePath, 'w') as f:
                            f.write('1\n')
                            f.write('%d %d %d %d %s' %(xmin,ymin,xmax,ymax,classLabel))
                            
            tkMessageBox.showinfo("Info", "XML parsing complete")
            self.clearBBox()
            self.loadBBox()'''
                       
                
    def loadBBox(self):
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    if i == 0:
                        bbox_cnt = int(line.strip())
                        continue
                    # tmp = [int(t.strip()) for t in line.split()]
                    tmp = line.split()
                    #print tmp
                    self.bboxList.append(tuple(tmp))
                    tmpId = self.mainPanel.create_rectangle(int(tmp[0]), int(tmp[1]), \
                                                            int(tmp[2]), int(tmp[3]), \
                                                            width = 2, \
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    # print tmpId
                    self.bboxIdList.append(tmpId)
                    self.listbox.insert(END, '%s : (%d, %d) -> (%d, %d)' %(tmp[4],int(tmp[0]), int(tmp[1]), \
                    												  int(tmp[2]), int(tmp[3])))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
    
    def loadCheckpoint(self, event = None):
        checkpoint = 0
        with open("log/checkpoint.txt","r") as checkpointFile:
            checkpoint = checkpointFile.read()
        if 1 <= int(checkpoint) and int(checkpoint) <= self.total:
            self.cur = int(checkpoint)
            self.loadImage()
    
    def resetCheckpoint(self, event = None):
        with open("log/checkpoint.txt","w") as checkpointFile:
            checkpointFile.write("1")

    def prevImage(self, event = None):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        with open("log/checkpoint.txt","w") as checkpointFile:
            checkpointFile.write("{}".format(self.cur))
            print "Current image : "+self.imageList[self.cur-1]
            
    def skipImage(self, event = None):
        #os.remove(self.imageList[self.cur - 1])
        print self.imageList[self.cur - 1]+" is skipped."
        with open("log/skipped.txt",'a') as skippedFile:
            skippedFile.write("{}\n".format(self.imageList[self.cur - 1]))
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

    def setClass(self, event):
        self.currentLabelclass = self.classcandidate.get()
        print 'set label class to :',self.currentLabelclass
        
    def setClassShortcut(self, event):
        if (event.char.isdigit()):
            idx = int(event.char) - 1
            print idx
            self.classcandidate.current(idx)
            self.currentLabelclass = self.classcandidate.get()
            print 'set label class to :',self.currentLabelclass
        
    def convert2Yolo(self, event = None):
        if (self.category == ''):
            tkMessageBox.showinfo("Error", "Please Annotate Image first")
        else:
            outpath = "./Result_YOLO/" + self.category +'/'
            convert.Convert2Yolo(self.outDir+'/', outpath, self.category, self.cla_can_temp)
            tkMessageBox.showinfo("Info", "YOLO data format conversion done")
        

##    def setImage(self, imagepath = r'test2.png'):
##        self.img = Image.open(imagepath)
##        self.tkimg = ImageTk.PhotoImage(self.img)
##        self.mainPanel.config(width = self.tkimg.width())
##        self.mainPanel.config(height = self.tkimg.height())
##        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)

if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
    root.resizable(width =  True, height = True)
    root.mainloop()
