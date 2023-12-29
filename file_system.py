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

def save_image(processed_frame, path, name):
    image = processed_frame[0]
    save_frame(image, path, name)
    
def save_video(processed_frames, path, name):
    img_array = []
    for processed_frame in processed_frames:
        height, width, _ = processed_frame.shape
        size = (width,height)
        img_array.append(processed_frame)
    out = cv.VideoWriter(path + f'/{name}', cv.VideoWriter_fourcc(*'mp4v'), 30, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    
    out.release()
    