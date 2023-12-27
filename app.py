import tkinter as tk
import ttkbootstrap as ttk
import cv2 as cv
from PIL import Image,ImageTk
import face_recognition as fr
import input_options_frame as iof

def open_camera():
    
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_with_faces = fr.detect_faces(frame)
        cv.imshow('Face Detection', frame_with_faces)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

def convert():
    output_string.set(selected_input.get())

# window
window = ttk.Window(themename='journal')
window.title('Age detection')
window.geometry('1600x900')
window.minsize(width='800', height='450')
window.bind('<Escape>', lambda e: window.quit())

# input options
option_frame, selected_input = iof.get_options_frame(window)
option_frame.pack()


#input field
input_frame = ttk.Frame(master = window)
button = ttk.Button(master = input_frame, text = 'Run', command=convert)
button.pack()
input_frame.pack(pady=10)

#output label
output_string = tk.StringVar()
output_label = ttk.Label(master=window, text='Output', font='Calibri 24', textvariable=output_string)
output_label.pack(pady=5)

#run
window.mainloop()