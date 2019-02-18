Main Program forked from [puzzledqs/BBox-Label-Tool](https://github.com/puzzledqs/BBox-Label-Tool/tree/multi-class)<br>
Converting to Yolo format forked from [ManivannanMurugavel/YOLO-Annotation-Tool] (https://github.com/ManivannanMurugavel/YOLO-Annotation-Tool)
## Feature
1. Multi-class support 
2. Support '.JPG' format

Data Organization
-----------------
LabelTool  
|  
|--main.py   *# source code for the tool*  
|  
|--Images/   *# direcotry containing the images to be labeled*  
   |--1/     *# project name  
|--Labels/   *# direcotry for the labeling results*  
   |--1/     *# result txt according to project name
   |--output/*# converted to YOLO format
|--Examples/  *# direcotry for the example bboxes* 

BBox-Label-Tool
===============

A simple tool for labeling object bounding boxes in images, implemented with Python Tkinter. 

Dependency
----------
python 2.7 win 32bit
PIL-1.1.7.win32-py2.7

## Usage
1. For multi-class task, modify 'class.txt' with your own class-candidates and before labeling bbox, choose the 'Current Class' in the Combobox and make sure you click 'ComfirmClass' button.
2. run `python main.py` 
3. Input a number according to project name (e.g, 1, 2, 5...), and click 'Load'. The images along with a few example results will be loaded.
4. To create a new bounding box, left-click to select the first vertex. Moving the mouse to draw a rectangle, and left-click again to select the second vertex.
  - To cancel the bounding box while drawing, just press <Esc>.
  - To delete a existing bounding box, select it from the listbox, and click 'Delete'.
  - To delete all existing bounding boxes in the image, simply click 'ClearAll'.
5. After finishing one image, click 'Next' to advance. Likewise, click 'Prev' to reverse. Or, input the index and click 'Go' to navigate to an arbitrary image.
  - The labeling result will be saved in **Labels/1/..** if and only if the 'Next' button is clicked.
6. run `python convert.py` to convert the labeling result to YOLO format. The result will be saved in **Labels/Output/..**
