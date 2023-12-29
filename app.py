from tkinter import *
from tkdocviewer import *
import ttkbootstrap as ttk
import cv2 as cv
from PIL import Image,ImageTk
import face_recognition as fr
import input_options_frame as iof
from input_options import InputOptions
from tkinter import filedialog

def browse_files():
    filepath = filedialog.askopenfilename(initialdir='/', title='Select a file')
    return filepath

# window
window = ttk.Window(themename='journal')
window.title('Age detection')
window.geometry('1600x900')
window.minsize(width='800', height='450')
window.bind('<Escape>', lambda e: window.quit())

# input options
option_frame, selected_input = iof.get_options_frame(window)
option_frame.pack()

label_widget = ttk.Label(window)
label_widget.pack()

#v = DocViewer(window)
#v.pack(side="top", expand=1, fill="both")
#path = browse_files()
#v.display_file(path)


# camera
vid = cv.VideoCapture(1)
width, height = 800, 450
vid.set(cv.CAP_PROP_FRAME_WIDTH,width)
vid.set(cv.CAP_PROP_FRAME_HEIGHT,height)

def display_output(frame):
    # Convert image from one color space to other 
    opencv_image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA) 
  
    # Capture the latest frame and transform to image 
    captured_image = Image.fromarray(opencv_image) 
  
    # Convert captured image to photoimage 
    photo_image = ImageTk.PhotoImage(image=captured_image) 
  
    # Displaying photoimage in the label 
    label_widget.photo_image = photo_image 
  
    # Configure image in the label 
    label_widget.configure(image=photo_image) 
    

def open_camera():

    if(selected_input.get() != InputOptions.CAMERA.name):
        label_widget.photo_image = None
        return
  
    _, frame = vid.read()
    frame = fr.detect_faces(frame)
    display_output(frame)
    label_widget.after(10, open_camera) 
  
def read_photos():
    
    file_path = browse_files()
    image = cv.imread(file_path)
    if image is not None:
        frame = fr.detect_faces(image)
        display_output(frame)
    else:
        print("Nie można odczytać obrazu.")
    
    


def run():
    arg = selected_input.get()
    
    if(arg == InputOptions.CAMERA.name):
        open_camera()
    elif(arg == InputOptions.PHOTOS.name):
        read_photos()
    elif(arg == InputOptions.VIDEO.name):
        print('video')
  

run_button = ttk.Button(window, text="Run", command=run) 
run_button.pack() 

#run
window.mainloop()