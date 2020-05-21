# AnnotatorCanvas

### Overview
---
Implemented as a quick and easy aid for point and polygonal image annotation. Originally intended for use with tissue sample annotation, and is inspired by wkentaro's [labelme](https://github.com/wkentaro/labelme) project. <br>
AnnotatorCanvas is written in Python 3.7 and uses tkinter. <br><br>


<a href="https://imgur.com/OvqPmSf"><img src="https://i.imgur.com/OvqPmSf.png" title="sampleAnnotation" /></a><br>
_The absolutely low-res figure above shows an example of a squamous epithelium sample (source: wikimedia) that has been annotated._

### Requirements
---
* Python 3.6 and above
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

#### Methods
`annotate_point()`<br>
Sets the AnnotatorCanvas for point annotation. A left-click is bound to the addition of a point, while the backspace key is bound to the undoing of a point.
<br>

`annotate_polygon()`
<br>
Sets the AnnotatorCanvas for polygonal annotation. A left-click is bound to the addition of a polygon node, a double-left-click closes the polygon, and the the backspace key is bound to the undo method. 
<br>

`clear_all()`
<br>
As the method name suggests, all points and polygons are deleted off.
<br>

`flush()`
<br>
Call this method when annotation of an image has finished. Flushes all saved points and polygons into a dictionary with keys `points` and `polygons`. The AnnotatorCanvas and its internal storage is cleared.
<br>

`unbind_all()`
<br>
Not entirely sure why I put this method here, but perhaps call it if there is a need to unbind all the keyboard/mouse shortcuts.
<br>

The rest of the methods are simply helper methods.

#### To Note
* The polygons and points are kept on separate "layers". In other words, points are "undone" independent of the polygons, and vice versa.
* If `annotate_point()` is called while there is an unclosed polygon, the polygon will be automatically closed by joining the last polygon node created with the first polygon node.
* Polygon closure will only occur if there are more than **two** points of the polygon when a double-left-click is encountered. The unfinished polygon will be treated as an anomaly and discarded otherwise.
* Undoing while all polygons are closed will undo an entire polygon.
* Undoing while there is an unclosed polygon will undo a single line.