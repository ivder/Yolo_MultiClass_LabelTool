My own version of labeling tool for YOLO format (support Multi Class labeling on the same image)

Main Program forked from [puzzledqs/BBox-Label-Tool](https://github.com/puzzledqs/BBox-Label-Tool/tree/multi-class)<br>
Converter to Yolo format forked from [ManivannanMurugavel/YOLO-Annotation-Tool] (https://github.com/ManivannanMurugavel/YOLO-Annotation-Tool)<br>
**Changed 001 as a project name instead of class name**

## Feature
1. Multi-class support 
2. Support '.JPG' format

## Additional Feature
1. Skip button to skip labeling on unwanted image
2. Add Save and Load Checkpoint
3. Remove class confirm button (set value directly from combobox)

Data Organization
-----------------
LabelTool  
|  
|--main.py   *# source code for the tool*  
|--Images/   *# direcotry containing the images to be labeled* 
&nbsp;    |--1/     *# project name  
|--Labels/   *# direcotry for the labeling results*  
&nbsp;&nbsp;&nbsp;|--1/     *# result txt according to project name <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|--output/*# converted to YOLO format<br>
|--Examples/  *# direcotry for the example bboxes* 

BBox-Label-Tool
===============

A simple tool for labeling object bounding boxes in images, implemented with Python Tkinter. 

Dependency
----------
python 2.7 win 32bit
PIL-1.1.7.win32-py2.7

## Usage
1. For multi-class task, modify 'class.txt' with your own class-candidates and before labeling bbox, choose the 'Current Class' in the Combobox.
2. run `python main.py` 
3. Input a number according to project name (e.g, 1, 2, 5...), and click `Load`. The images along with a few example results will be loaded.
4. To create a new bounding box, left-click to select the first vertex. Moving the mouse to draw a rectangle, and left-click again to select the second vertex.
  - To cancel the bounding box while drawing, just press <Esc>.
  - To delete a existing bounding box, select it from the listbox, and click `Clear`.
  - To delete all existing bounding boxes in the image, simply click `ClearAll`.
5. After finishing one image, click `Next` to advance. Likewise, click `Prev` to reverse. Or, input the index and click `Go` to navigate to an arbitrary image.
   - The labeling result will be saved in **Labels/1/..** if and only if the 'Next' button is clicked.
   - **Checkpoint of last Image filepath will be saved when 'Next' button is clicked.**
6. Click `Skip` if you want to skip unwanted image from directory and skip the annotation for that image (skipped image path will be saved in log/skip.txt)
7. run `python convert.py` to convert the labeling result to YOLO format. The result will be saved in **Labels/Output/..**
   
**Output**

![Example](https://github.com/gameon67/Yolo_MultiClass_LabelTool/blob/master/Examples/demo/Capture.JPG)

    1 0.4203125 0.613888888889 0.090625 0.0722222222222
    3 0.730729166667 0.683333333333 0.0364583333333 0.162962962963
