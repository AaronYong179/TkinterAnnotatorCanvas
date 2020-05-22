# AnnotatorCanvas

### Overview
---
Implemented as a quick and easy aid for point and polygonal image annotation. Originally intended for use with tissue sample annotation, and is inspired by wkentaro's [labelme](https://github.com/wkentaro/labelme) project. <br>
AnnotatorCanvas is written in Python 3.7 and uses tkinter. <br><br>


<a href="https://imgur.com/OvqPmSf"><img src="https://i.imgur.com/OvqPmSf.png" title="sampleAnnotation" /></a><br>
_The absolutely low-res figure above shows an example of a squamous epithelium sample (source: wikimedia) that has been annotated._

### Requirements
---
* Python 3.6 and above (or just delete the f-strings and it should work on Python3.x I think)
* [tkinter](https://docs.python.org/3/library/tkinter.html)

### Importing 
---
Simply copy/paste the entire class, or one could keep ```AnnotatorCanvas.py``` separate and call ```from AnnotatorCanvas import AnnotatorCanvas``` instead.


### Usage
---
The AnnotatorCanvas extends tkinter's Canvas widget, hence inherits all methods already present in Canvas. Read the documentation for Canvas [here](https://effbot.org/tkinterbook/canvas.htm).
<br><br>
_Example instantiation:_
```
class MainApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # Instantiate AnnotatorCanvas as you would for Canvas
        self.annotator = AnnotatorCanvas(master, bg="black", width=800, height=600)
        self.annotator.pack()
```

#### Constants
`LINE_COLOUR`
<br>
Sets the colour used for annotation. Default value: yellow
<br>

`LINE_WIDTH`
<br>
Sets the width of the annotated lines. Default value: 2
<br>

`POINT_RAD`
<br>
Sets the radius of the point created. Default value: 2
<br>

_Example modification of constants_
```
annotator = AnnotatorCanvas(root)
annotator.LINE_COLOUR = "red"
annotator.LINE_WIDTH = 1
annotator.POINT_RAD = 1
```

#### Methods
`annotate_point()`
<br>
Sets the AnnotatorCanvas for point annotation. 
* A left-click is bound to the addition of a point
* The BackSpace key is bound to the `undo_point` method.
<br>

`undo_point()`
<br>
Bound to the BackSpace key. Simply deletes the last point placed. The polygons and points are kept on separate "layers". In other words, points are "undone" independent of the polygons, and vice versa.
<br><br>

`annotate_polygon()`
<br>
Sets the AnnotatorCanvas for polygonal annotation. 
* A left-click is bound to the addition of a polygon node.
* A double-left-click closes the polygon (**polygon closure**).
* The BackSpace key is bound to the `undo_polygon` method. 
* Additional note on annotating polygons:
  * Polygon closure will only occur if there are more than two points of the polygon when a double-left-click is encountered. The unfinished polygon will be treated as an anomaly and discarded otherwise.
  * If `annotate_point()` is called while there is an unclosed polygon, the polygon will be automatically closed by joining the last polygon node created with the first polygon node.
<br>

`undo_polygon()`
<br>
Bound to the BackSpace key. 
* Additional note on undoing polygons:
  * Undoing while all polygons are closed will undo an entire polygon.
  * Undoing while there is an unclosed polygon will undo a single line.

The polygons and points are kept on separate "layers". In other words, points are "undone" independent of the polygons, and vice versa.<br><br>

`clear_all()`
<br>
As the method name suggests, all points and polygons are deleted off.
<br><br>

`flush()`
<br>
Call this method when annotation of an image has finished. Flushes all saved points and polygons into a dictionary with keys `points` and `polygons`. The AnnotatorCanvas and its internal storage is cleared.
<br><br>

`unbind_all()`
<br>
Call this method to unbind all keyboard shortcuts implemented by AnnotatorCanvas
<br><br>

`set_boundary(x, y, width, height)`
<br><br>
Only call this method if there is a need to specify a rectangle on the canvas where annotation is allowed. Otherwise, the entire canvas will be made available for annotation. 
Perhaps this can be used in conjunction with some form of a marquee tool. 
<br><br>

`is_within_boundary(x, y)`
<br>
Checks if the input x and y coordinates are within the demarcated boundary. If no boundary was previously set, this method simply returns `True`.
<br><br>

The rest of the methods are simply helper methods.