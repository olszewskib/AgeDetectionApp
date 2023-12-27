import tkinter as tk
import ttkbootstrap as ttk
import cv2 as cv
from PIL import Image,ImageTk
import face_recognition as fr
import input_options_frame as iof
from input_options import InputOptions

# window
window = ttk.Window(themename='journal')
window.title('Age detection')
window.geometry('1600x900')
window.minsize(width='800', height='450')
window.bind('<Escape>', lambda e: window.quit())

# input options
option_frame, selected_input = iof.get_options_frame(window)
option_frame.pack()

# camera
vid = cv.VideoCapture(1)
width, height = 800, 450
vid.set(cv.CAP_PROP_FRAME_WIDTH,width)
vid.set(cv.CAP_PROP_FRAME_HEIGHT,height)

label_widget = ttk.Label(window)
label_widget.pack()

def open_camera():
    
    if(selected_input.get() != InputOptions.CAMERA.name):
        label_widget.photo_image = None
        return
  
    # Capture the video frame by frame 
    _, frame = vid.read()
    
    frame = fr.detect_faces(frame)
  
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
  
    # Repeat the same process after every 10 mseconds 
    label_widget.after(10, open_camera) 
  
  
# Create a button to open the camera in GUI app 
run_button = ttk.Button(window, text="Run", command=open_camera) 
run_button.pack() 

#run
window.mainloop()