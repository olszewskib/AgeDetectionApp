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

def save_images(processed_frames):
    path = browse_directories()
    i = 0 #TODO fix file names
    for processed_photo in processed_frames:
        save_frame(processed_photo, path, f'test{i}')
        i+=1
    
def save_camera_input(processed_frames, filename):
    path = browse_directories()

    img_array = []
    for processed_frame in processed_frames:
        height, width, _ = processed_frame.shape
        size = (width,height)
        img_array.append(processed_frame)
    out = cv.VideoWriter(path + f'/{filename}.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    
    out.release()
    