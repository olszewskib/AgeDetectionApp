from tkinter import *
from tkdocviewer import *
import ttkbootstrap as ttk
import cv2 as cv
from PIL import Image,ImageTk
import face_recognition as fr
import input_options_frame as iof
from input_options import InputOptions
from tkinter import filedialog
import glob

# Globals
PADDING = 15
processed_photos = []

def browse_files():
    filepath = filedialog.askopenfilename(initialdir='/', title='Select a file')
    return filepath

def browse_directories():
    dirpath = filedialog.askdirectory(initialdir='/', title='Select directory')
    return dirpath

def on_resize(event):
    if(selected_input.get() == InputOptions.CAMERA.name):
        pass

# window
window = ttk.Window(themename='journal')
window.title('Age detection')
window.geometry('1600x900')
window.minsize(width='800', height='450')
window.bind('<Escape>', lambda e: window.quit())
window.bind('<Configure>', on_resize)

# input options
option_frame, selected_input = iof.get_options_frame(window)
option_frame.pack(side='left', padx=PADDING, pady=PADDING, fill='both')

label_widget = ttk.Label(window)
label_widget.pack(side='right', padx=PADDING, pady=PADDING, expand=True)

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
    
    processed_photos.clear()
    files_listbox.delete(0, END)
    dir_path = browse_directories()
    file_paths = glob.glob(dir_path + '/*.jpg')

    for file_path in file_paths:
        processed_photo = process_photo(file_path)
        processed_photos.insert(0,processed_photo)
        file_name = file_path.split('/')[-1]
        files_listbox.insert(0, file_name)
    
    return processed_photos

def process_photo(file_path):
    
    image = cv.imread(file_path)
    if image is not None:
        frame = fr.detect_faces(image)
        display_output(frame)
        return frame
    else:
        print("Not a valid image")
    
def run():
    arg = selected_input.get()
    
    if(arg == InputOptions.CAMERA.name):
        open_camera()
    elif(arg == InputOptions.PHOTOS.name):
        read_photos()
    elif(arg == InputOptions.VIDEO.name):
        print('video')
  

run_button = ttk.Button(option_frame, text="Run", command=run) 
run_button.pack(pady=PADDING) 

files_title_label = ttk.Label(master = option_frame, text = 'Files', font = 'Calibri 24 bold').pack(anchor='w')
files_listbox = Listbox(option_frame, height=200) # fix height with a constant value
files_listbox.bind('<<ListboxSelect>>', lambda e: display_output(processed_photos[files_listbox.curselection()[0]]))
    
files_listbox.pack(pady=PADDING)

#run
window.mainloop()