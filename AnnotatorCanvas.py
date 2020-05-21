import tkinter as tk
from PIL import ImageTk

class AnnotatorCanvas(tk.Canvas):
    LINE_COLOUR = "yellow"
    LINE_WIDTH = 2
    POINT_RAD = 2
    
    def __init__(self, master=None, **Options):
        super().__init__(master, **Options)
        self.saved_points = []
        self.points = []
        
        self.saved_polygons = []
        self.polygon_coords = []
        self.lines = {}

    def print_all(self):
        # for debugging
        print(f"saved_points: {self.saved_points}")
        print(f"saved_polygons: {self.saved_polygons}")

    def flush(self):
        output = {"points": list(set(self.saved_points)),
                  "polygons": self.saved_polygons}
        self.clear_all()
        self.unbind_all()
        return output

    def clear_all(self):
        self.delete("all")
        self.saved_points = []
        self.points = []
        
        self.saved_polygons = []
        self.polygon_coords = []
        self.lines = {}

    def unbind_all(self):
        self.unbind("<Button-1>")
        self.unbind("<Double-Button-1>")
        self.master.unbind("<BackSpace>")


    ######################################
    ##   METHODS FOR POINT ANNOTATION   ##
    ######################################

    def annotate_point(self):
        if self.polygon_coords:
            self.close_polygon("_")
            
        self.bind("<Button-1>", self.add_point)
        self.unbind("<Double-Button-1>")
        self.master.bind("<BackSpace>", self.undo_point)

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append(self.create_oval(x, y, x + self.POINT_RAD, y + self.POINT_RAD, outline=self.LINE_COLOUR, width=self.LINE_WIDTH))
        self.saved_points.append((x, y))

    def undo_point(self, event):
        if self.saved_points:
            del self.saved_points[-1]
            self.delete(self.points.pop(-1))
    

    ######################################
    ## METHODS FOR POLYGONAL ANNOTATION ##
    ######################################

    """ The UX for polygonal annotation is largely referenced from Adobe Photoshop's Lasso Tool. """

    def annotate_polygon(self):
        self.polygon_coords =[]
        self.bind("<Button-1>", self.add_node)
        self.bind("<Double-Button-1>", self.close_polygon)
        self.master.bind("<BackSpace>", self.undo_polygon)

    def add_node(self, event):
        x, y = event.x, event.y
        if self.polygon_coords:
            last_x = self.polygon_coords[-1][0]; last_y = self.polygon_coords[-1][1]
            self._create_line(last_x, last_y, x, y)
        self.polygon_coords.append((x, y))

    def close_polygon(self, event):
        """
        Automatically closes the drawn polygon if it is 2-dimensional. 1-dimensional annotations are
        treated as anomalous and are deleted if this method is called.

        The closed polygon is saved into :attr self.saved_polygons.
        """
        if len(self.polygon_coords) <= 2:
            while self.polygon_coords:
                self.undo_polygon("_")
            return
        
        first_x = self.polygon_coords[0][0]; first_y = self.polygon_coords[0][1]
        last_x = self.polygon_coords[-1][0]; last_y = self.polygon_coords[-1][1]

        self._create_line(last_x, last_y, first_x, first_y)                                                        
        self.saved_polygons.append(self.polygon_coords)
        self.polygon_coords = []

    def undo_polygon(self, event):
        if self.polygon_coords:
            self.delete_last_point(self.polygon_coords)
        elif self.saved_polygons:
            self.delete_last_polygon()

    def _create_line(self, x1, y1, x2, y2):
        line = self.create_line(x1, y1, x2, y2, fill=self.LINE_COLOUR, width=self.LINE_WIDTH)
        self.lines[((x1, y1), (x2, y2))] = line

    def delete_last_point(self, coordinates_list):
        """
        Deletes the last point created. If there is an associated line, the line will be removed
        from the canvas as well.
        """
        if len(coordinates_list) == 1:
            del coordinates_list[-1]
        else:
            self._delete_last_line(coordinates_list)

    def delete_last_polygon(self):
        last_polygon = self.saved_polygons.pop(-1)
        # Append the first point to the back, to delete the polygon's lines properly.
        last_polygon.append(last_polygon[0])
        while len(last_polygon) >= 1:
            self.delete_last_point(last_polygon)
        
    def _delete_last_line(self, coordinate_list):
        """
        Private helper method. Deletes the last line given a list of polygon points.

        Parameter
        ---------
        coordinate_list : List
            This implemetation assumes that the coordinate_list given must contain at
            least one line. In other words, the coordinate_list must contain at least
            two points.
        """
        x2, y2 = coordinate_list.pop(-1)
        x1, y1 = coordinate_list[-1]   
        line = self.lines.pop( ((x1, y1), (x2, y2)) )
        self.delete(line)




    
