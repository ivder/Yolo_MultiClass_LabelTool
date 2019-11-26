My own version of labeling tool for YOLO format (support Multi Class labeling on the same image)

Main Program forked from [puzzledqs/BBox-Label-Tool](https://github.com/puzzledqs/BBox-Label-Tool/tree/multi-class)<br>
Converter to Yolo format forked from [ManivannanMurugavel/YOLO-Annotation-Tool] (https://github.com/ManivannanMurugavel/YOLO-Annotation-Tool)<br>

## Feature
1. Multi-class support 
2. Support '.JPG' format
3. Built in YOLO format converter

## Additional Feature
1. Skip button to skip labeling on unwanted image
2. Add Save and Load Checkpoint
3. Remove class confirm button (set value directly from combobox)
4. Add Convert to YOLO format button (no need to run external program)
5. Load image using directory browser instead of user input

Data Organization
-----------------
LabelTool  
|  
|--main.py                    *# source code for the tool*  
|--Images/                    *# direcotry containing the images to be labeled* <br>
&nbsp;&nbsp;&nbsp;|--Sample/               *# project/directory name*  
|--Result/                    *# direcotry for the labeling results*  
&nbsp;&nbsp;&nbsp;|--Sample/       *# result txt according to project name* <br>
|--Result_YOLO/               *# converted to YOLO format*<br>

Yolo Annotator
===============

A simple tool for labeling object bounding boxes in images, implemented with Python Tkinter. 

Dependency
----------
python 2.7 win 32bit
PIL-1.1.7.win32-py2.7

## Usage
1. For multi-class task, modify 'class.txt' with your own class-candidates and before labeling bbox, choose the 'Current Class' in the Combobox or by pressing <kbd>1-9</kbd> on your keyboard.
2. run `python main.py` 
3. click `LoadImage`, select a folder that contains list of images.
4. To create a new bounding box, left-click to select the first vertex. Moving the mouse to draw a rectangle, and left-click again to select the second vertex.
  - To cancel the bounding box while drawing, just press <kbd>Esc</kbd> or <kbd>s</kbd>.
  - To delete a existing bounding box, select it from the listbox, and click `Clear` or <kbd>r</kbd>.
  - To delete all existing bounding boxes in the image, simply click `ClearAll`.
5. After finishing one image, click `Next` or <kbd>d</kbd> to advance. Likewise, click `Prev` or <kbd>a</kbd> to reverse. Or, input the index and click `Go` to navigate to an arbitrary image.
   - The labeling result will be saved in **Labels/[folder name]/..** if and only if the 'Next' button is clicked.
   - **Checkpoint of last Image Number will be saved when 'Next' button is clicked.**
6. Click `Skip` if you want to skip unwanted image from directory and skip the annotation for that image (skipped image path will be saved in log/skip.txt)
7. Click `ConvertYOLO` button or to convert the labeling result to YOLO format. The result will be saved in **Result_YOLO/[folder name]/..**
   
**Output**

![Example](https://github.com/gameon67/Yolo_MultiClass_LabelTool/blob/master/Examples/Capture.JPG)

Result (bbox coodrdinates):
```
2
99 17 571 436 dog
733 60 988 320 cat
```
Result_YOLO (yolo format) : 
```
0 0.279166666667 0.359523809524 0.393333333333 0.665079365079
1 0.717083333333 0.301587301587 0.2125 0.412698412698
```

