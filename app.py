import glob
import queue
import threading
from tkinter import *

import cv2 as cv
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from tkdocviewer import *

import face_recognition as fr
import input_options_frame as iof
from file_system import *
from input_options import InputOptions

# Globals
PADDING = 15
CAMERA_VIDEO_NAME = "camera"
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
processed_frames = []
preview_buffer = []

# listbox files
files = []
files.append([])  # sentinel

# live feed from camera
frame_queue = queue.Queue()


def on_resize(e):
    update_gui()


# window
window = ttk.Window(themename="journal")
window.title("Age detection")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.minsize(width="800", height="450")
window.bind("<Escape>", lambda e: window.quit())
window.bind("<Configure>", on_resize)

# input options
option_frame, selected_input = iof.get_options_frame(window)
option_frame.pack(side="left", padx=PADDING, pady=PADDING, fill="both")

# Create a canvas and put it in a scrollbar
v_scrollbar = ttk.Scrollbar(window, orient="vertical")
v_scrollbar.pack(side="right", fill="y")

h_scrollbar = ttk.Scrollbar(window, orient="horizontal")
h_scrollbar.pack(side="bottom", fill="x")

canvas = ttk.Canvas(
    window, yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
)
canvas.pack(side="left", fill="both", expand=True)

v_scrollbar.config(command=canvas.yview)
h_scrollbar.config(command=canvas.xview)

# Create a frame inside the canvas and put the label in it
frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

label_widget = ttk.Label(frame)
label_widget.pack(side="right", padx=PADDING, pady=PADDING, expand=True)


# Update the scrollregion of the canvas when the size of the frame changes
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


frame.bind("<Configure>", on_frame_configure)


def start_video_capture():
    capture_thread = threading.Thread(target=video_capture)
    capture_thread.start()
    update_gui()


def video_capture():
    vid = cv.VideoCapture(0)
    width, height = WINDOW_WIDTH, WINDOW_HEIGHT
    vid.set(cv.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv.CAP_PROP_FRAME_HEIGHT, height)

    while selected_input.get() == InputOptions.CAMERA.name:
        _, frame = vid.read()
        frame = fr.detect_faces(frame)
        processed_frames.append(frame)
        label_widget.after(10, update_gui)
        frame_queue.put(frame)

    vid.release()


def update_gui():
    if frame_queue.empty() or selected_input.get() != InputOptions.CAMERA.name:
        return

    frame = frame_queue.get_nowait()
    display_output(frame)


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
    if selected_input.get() != InputOptions.CAMERA.name:
        processed_frames.clear()
        label_widget.photo_image = None
        return

    start_video_capture()


def process_photo(file_path):
    image = cv.imread(file_path)
    frame = fr.detect_faces(image)
    display_output(frame)
    return frame


def load_photos():
    # loading photos photos
    dir_path = browse_directories()
    file_paths = glob.glob(dir_path + "/*.jpg")
    file_paths += glob.glob(dir_path + "/*.jpeg")
    file_paths += glob.glob(dir_path + "/*.png")
    file_paths += glob.glob(dir_path + "/*.bmp")

    for file_path in file_paths:
        processed_frame = [process_photo(file_path)]

        # adding file to listbox
        file_name = file_path.split("/")[-1]
        listbox.insert(1, file_name)
        # adding corresponding file to files
        files.insert(1, processed_frame)

    # clearing processed frames
    processed_frames.clear()

    # selecting most recent file
    listbox.selection_clear(0, END)
    listbox.selection_set(1)


def load_camera_input():
    # adding an entry to a listbox
    listbox.insert(1, CAMERA_VIDEO_NAME + str(len(files)) + ".mp4")

    # adding corresponding file to files
    tmp = []
    for frame in processed_frames:
        tmp.append(frame)
    files.insert(1, tmp)

    # clearting processed frames
    processed_frames.clear()


def load_video():
    file_path = browse_files()

    processed_frames.clear()
    capture = cv.VideoCapture(file_path)
    while True:
        success, frame = capture.read()
        if success:
            processed_frame = fr.detect_faces(frame)
            processed_frames.append(processed_frame)
        else:
            break

    capture.release()

    # adding an entry to a listbox
    file_name = file_path.split("/")[-1]
    listbox.insert(1, file_name)

    # adding corresponding file to files
    tmp = []
    for frame in processed_frames:
        tmp.append(frame)
    files.insert(1, tmp)

    # clearting processed frames
    processed_frames.clear()


def preview_file():
    if len(preview_buffer) == 0:
        return
    img = preview_buffer.pop(0)
    display_output(img)
    label_widget.after(10, preview_file)


def delete_selected():
    global camera_on
    if camera_on:
        selected_input.set(InputOptions.SAVING.name)
        processed_frames.clear()
        delete_button_description.set("delete")
        camera_on = False
        return

    indices = listbox.curselection()
    if len(indices) == 0 or indices[0] == 0:
        return

    for index in reversed(indices):
        listbox.delete(index)
        files.pop(index)


def save_selected():
    indices = listbox.curselection()
    if len(indices) == 0 or indices[0] == 0:
        return

    path = browse_directories()
    for index in reversed(indices):
        file = files[index]
        name = listbox.get(index)
        if len(file) > 1:
            save_video(file, path, name)
        else:
            save_image(file, path, name)


def on_listbox_select(e):
    index = listbox.curselection()[0]

    if index == 0:
        listbox.select_clear(0, END)
        listbox.select_set(1, END)
        return

    file_to_preview = files[index]
    for frame in file_to_preview:
        preview_buffer.append(frame)

    preview_file()


def save_files():
    arg = selected_input.get()

    if arg == InputOptions.CAMERA.name:
        selected_input.set(InputOptions.SAVING.name)
        load_camera_input()
        selected_input.set(InputOptions.CAMERA.name)
    else:
        save_selected()


camera_on = False


def run():
    global camera_on
    arg = selected_input.get()

    if arg == InputOptions.CAMERA.name:
        camera_on = True
        delete_button_description.set("stop")
        save_button_description.set("save")
        open_camera()
    elif arg == InputOptions.PHOTOS.name:
        camera_on = False
        delete_button_description.set("delete")
        save_button_description.set("save all")
        load_photos()
    elif arg == InputOptions.VIDEO.name:
        camera_on = False
        delete_button_description.set("delete")
        load_video()


run_button = ttk.Button(option_frame, text="select", command=run).pack(pady=PADDING)

files_title_label = ttk.Label(
    master=option_frame, text="Files", font="Calibri 24 bold"
).pack(anchor="w")
listbox = Listbox(option_frame)
listbox.insert(0, "all")
listbox.bind("<<ListboxSelect>>", on_listbox_select)
listbox.pack(pady=PADDING, expand=True, fill="y")

save_button_description = StringVar()
save_button_description.set("save")
save_button = ttk.Button(
    option_frame, textvariable=save_button_description, command=save_files
).pack(side="left")

delete_button_description = StringVar()
delete_button_description.set("delete")
delete_button = ttk.Button(
    option_frame, textvariable=delete_button_description, command=delete_selected
).pack(side="left", padx=PADDING)

# centering window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width / 2) - (WINDOW_WIDTH / 2)
y = (screen_height / 2) - (WINDOW_HEIGHT / 2)

window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(x)}+{int(y)}")

# run
window.mainloop(),
