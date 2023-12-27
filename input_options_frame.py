import tkinter as tk
import ttkbootstrap as ttk
from input_options import InputOptions

def get_options_frame(window):
    options_frame = ttk.Frame(master=window, borderwidth=10, relief=tk.GROOVE)
    options_frame_title_label = ttk.Label(master = options_frame, text = 'Input options', font = 'Calibri 24 bold').pack()

    input_option_var = tk.StringVar()

    camera_input_radio = ttk.Radiobutton(
        options_frame,
        variable=input_option_var,
        text='Camera',
        value=InputOptions.CAMERA.name
        ).pack(anchor='w')

    video_input_radio = ttk.Radiobutton(
        options_frame,
        variable=input_option_var,
        text='Video',
        value=InputOptions.VIDEO.name
        ).pack(anchor='w')
    
    photos_input_radio = ttk.Radiobutton(
        options_frame,
        variable=input_option_var,
        text='Photos',
        value=InputOptions.PHOTOS.name
        ).pack(anchor='w')

    return options_frame, input_option_var
