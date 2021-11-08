#import the tk library
from tkinter import *
#set the trace to 0 
trace = 0
    
print("Choose one of these colours for your shapes:black,white,green,red,blue,pink,cyan,orange,gold,brown,beige")
#decide which colours can be used in the program
colours =["black","white","green","red","blue","pink","cyan","orange","gold","brown","beige"]
#ask user for inputs for shape colours and ensure they are recognised colours
x=str(input("Enter the colour of the oval:"))    

while True:
        if x not in colours:
            print("ENTER ONE OF THE EXAMPLE COLOURS!!")
            x= str(input("Choose the colour of the oval:"))
            continue
        
        else:
            y= str(input("Choose the colour of the rectangle:"))
            break
while True:
        if y not in colours:
            print("ENTER ONE OF THE EXAMPLE COLOURS!!")
            y= str(input("Choose the colour of the rectangle:"))
            continue
        else:
            z= str(input("Choose the colour of the line:"))
            break

while True:
        if z not in colours:
            print("ENTER ONE OF THE EXAMPLE COLOURS!!")
            z= str(input("Choose the colour of the line:"))
            continue
        else:
            u = str(input("Choose the colour of the arrow:"))
            break
        
while True:
        if u not in colours:
            print("ENTER ONE OF THE EXAMPLE COLOURS!!")
            u= str(input("Choose the colour of the arrow:"))
            continue 
        else:
            w = str(input("Choose the colour of the arc:"))
            break
while True:
        if w in colours:
                break
        else:
                print("ENTER ONE OF THE EXAMPLE COLOURS!!")
                w = str(input("Choose the colour of the arc:"))
                continue 

class CanvasEvent:
    def __init__(self, parent=None):
#create toolbar and place it on canvas
        toolbar = Frame(bg='yellow')
        toolbar.pack(side='top', fill='y')
#set first shape on toolbar as the oval
        self.shapeVar = StringVar(value='oval')
#create canvas size and colour
        canvas = Canvas(width=1200, height=1200, bg='yellow')
        canvas.pack()
#bind mouse keys and actions to classes
        canvas.bind('<ButtonPress-1>', self.on_start)
        canvas.bind('<B1-Motion>', self.on_grow)
        canvas.bind('<Double-1>', self.on_clear)
        self.canvas = canvas
        self.drawn = None
#create dictionary for shapes
        self.kinds = {
            'oval': self.create_oval_tagged,
            'rectangle': self.create_rectangle_tagged,
            'line': self.create_line_tagged,
            'eraser': self.create_eraser_tagged,
            'arrow':self.create_arrow_tagged,
            'arc': self.create_arc_tagged,
        }
        shape_name = self.shapeVar.get()
        self.shape = self.kinds[shape_name]
#set initial data for item motion class 
        self.drag_data = {"x": 0, "y": 0, "item": None}

        def setShape():
            shape = self.shapeVar.get()
            self.shape = self.kinds[shape]
#associate toolbar buttons to buttons and classes
        shapes = ["oval", "rectangle", "line", "arrow", "arc", "eraser"]
        for shape in shapes:
            self.canvas.tag_bind(shape, "<ButtonPress-3>", self.on_item_press)
            self.canvas.tag_bind(shape, "<ButtonRelease-3>", self.on_item_release)
            self.canvas.tag_bind(shape, "<B3-Motion>", self.on_item_motion)

            button = Radiobutton(toolbar, text=shape, value=shape, indicatoron=False, variable=self.shapeVar, command=setShape)
            button.pack(side='left')
            
#create class for initial drawing the shapes            

    def on_item_press(self, event):
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
#create class for new data when shape is drawn
    def on_item_release(self, event):
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
#create class for when shape is being drawn, size etc
    def on_item_motion(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        self.canvas.move(self.drag_data["item"], delta_x, delta_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_start(self, event):
        self.start = event
        self.drawn = None

    def on_grow(self, event):
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = self.shape(self.start.x, self.start.y, event.x, event.y)
        if trace: print(objectId)
        self.drawn = objectId

    def on_clear(self, event):
        event.widget.delete('all')
        self.canvas.create_text(130, 50, text='Left click and drag to create a  shape')
        self.canvas.create_text(130, 85, text='Right click and drag a shape to Move it')
        self.canvas.create_text(130, 120, text='Double click to erase canvas')
        self.canvas.create_text(160, 150, text='Selected shape will go blue when mouse hovers on it')

class Move(CanvasEvent):
    def __init__(self, parent=None):
        CanvasEvent.__init__(self, parent)
        self.canvas.create_text(130, 50, text='Left click and drag to create a  shape')
        self.canvas.create_text(130, 85, text='Right click and drag a shape to Move it')
        self.canvas.create_text(130, 120, text='Double click to erase canvas')       
        self.canvas.create_text(160, 150, text='Selected shape will go blue when mouse hovers on it')

    def create_oval_tagged(self, x1, y1, x2, y2):
        object_id = self.canvas.create_oval(x1, y1, x2, y2)
        self.canvas.itemconfig(object_id, tag='oval', activefill="blue", fill=x)
        return object_id

    def create_rectangle_tagged(self, x1, y1, x2, y2):
        object_id = self.canvas.create_rectangle(x1, y1, x2, y2)
        self.canvas.itemconfig(object_id, tag='rectangle', activefill="blue", fill=y)
        return object_id

    def create_arrow_tagged(self, x1, y1, x2, y2):
        object_id = self.canvas.create_line(x1, y1, x2, y2)
        self.canvas.itemconfig(object_id, tag='arrow', activefill="blue", fill=u, arrow="last", width=5)
        return object_id

    def create_line_tagged(self, x1, y1, x2, y2):
        object_id = self.canvas.create_line(x1, y1, x2, y2)
        self.canvas.itemconfig(object_id, tag='line', activefill="blue", fill=z, width=7)
        return object_id

    def create_arc_tagged(self, x1, y1, x2, y2):
        object_id = self.canvas.create_arc(x1, y1, x2, y2)
        self.canvas.itemconfig(object_id, tag='arc', style="chord", activefill="blue", fill=w, start = "250" )
        return object_id

    def create_eraser_tagged(self, x1, y1, x2, y2):
        object_id = self.canvas.create_oval(x1, y1, x2, y2)
        self.canvas.itemconfig(object_id, tag='eraser', fill='yellow', outline ='yellow')
        return object_id

Move()


