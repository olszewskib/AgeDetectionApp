import tkinter as tk
import ttkbootstrap as ttk

def convert():
    mile_input = entry_int.get()
    km_output = mile_input * 1.61
    output_string.set(km_output)

# window
window = ttk.Window(themename='journal')
window.title('Age detection')
window.geometry('1600x900')
window.minsize(width='800', height='450')

# input options
options_frame = ttk.Frame(master=window, borderwidth=10, relief=tk.GROOVE)
options_frame_title_label = ttk.Label(master = options_frame, text = 'Input options', font = 'Calibri 24 bold').pack()
camera_label = ttk.Label(master=options_frame, text='Camera', font='Calibri 24').pack(anchor='w')
video_label = ttk.Label(master=options_frame, text='Video', font='Calibri 24').pack(anchor='w')
photos_label = ttk.Label(master=options_frame, text='Photo', font='Calibri 24').pack(anchor='w')
options_frame.pack()


#input field
input_frame = ttk.Frame(master = window)
entry_int = tk.IntVar()
entry = ttk.Entry(master = input_frame, textvariable=entry_int)
button = ttk.Button(master = input_frame, text = 'Convert', command=convert)
entry.pack(side='left', padx=10)
button.pack(side='left')
# input_frame.pack(pady=10)

#output label
output_string = tk.StringVar()
output_label = ttk.Label(master=window, text='Output', font='Calibri 24', textvariable=output_string)
output_label.pack(pady=5)

#run
window.mainloop()