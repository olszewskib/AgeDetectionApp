import cv2 as cv
from PIL import Image
from tkinter import filedialog


def browse_files():
    filepath = filedialog.askopenfilename(initialdir='/', title='Select a file')
    return filepath

def browse_directories():
    dirpath = filedialog.askdirectory(initialdir='/', title='Select directory')
    return dirpath

def save_frame(frame, path, name):
    opencv_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    image = Image.fromarray(opencv_image)
    image.save(path + f'/{name}.jpg')
