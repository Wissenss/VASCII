import cv2
from PIL import Image, ImageOps
import os
import sys
import tkinter as tk
from tkinter import filedialog as fd

"""CONVERTER LOGIC"""
ASCII_CHARS = ['@ ', '% ', '$ ', '# ', '* ', '+ ', '= ', '; ', ': ', ', ', '- ', '. ', '  ']

#
def resizeGrayImage(image, newWidth=70):
    width, height = image.size
    ratio = height/width
    newHeight = int(ratio*newWidth)
    image = ImageOps.grayscale(image.resize((newWidth, newHeight)))
    return image

def asciiImage(image):
    width, height = image.size
    pixels = list(image.getdata())

    frame = ""
    for i in range(height):
        for j in range(width):
            #frame += ASCII_CHARS[pixels[width*i + j]//20]
            frame += ASCII_CHARS[len(ASCII_CHARS)-(pixels[width*i + j]//20)-1]
        frame += "\n"
    frame += "\n\n"
    sys.stdout.write(frame)

    #frame = "\n".join([line for line in ])
    return image

def execute_txt(filename):
    name, extention = os.path.splitext(str(filename))
    print(filename)
    print(extention)
    print("done")

    if extention == ".mp4":
        source = cv2.VideoCapture(filename)

        while(source.isOpened()):
            ret, frame = source.read()
            image = Image.fromarray(frame)
            asciiImage(resizeGrayImage(image))
            if (not ret):
                break;
            cv2.imshow('video', frame)
            cv2.waitKey(10)
            #os.system("cls")
        source.release()
        cv2.destroyAllWindows()
    elif extention == ".jpg":
        source = Image.open(r"files/example_1.jpg")
        
        asciiImage(resizeGrayImage(source))
    else:
        return

root = tk.Tk()

"""APP SETUP"""
root.title("txt converter") #define title

#CENTER APP SCREEN
#get screen dimentions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#define initial app screen width and height
app_width = screen_width//2
app_height = screen_height//2

#get center coordinates
screen_width_center = int(screen_width/2 - app_width/2)
screen_height_center = int(screen_height/2 - app_height/2)

#position app screen in the center
root.geometry(f'{app_width}x{app_height}+{screen_width_center}+{screen_height_center}')

#RESIZABLE LIMITS
#allow resizability
root.resizable(True, True)

#set limits
root.minsize(app_width//2, app_height//2)
#root.maxsize(screen_width, screen_height)

"""GUI"""
global current_file
text = tk.StringVar()
text.set("Select a File!")

label = tk.Label(
    root, 
    textvariable=text
    )

def run():
    execute_txt(current_file)

run_button = tk.Button(
    root, 
    text = 'Load',
    command=run
)

def select_files():
    filetypes = (
        ('video files', '*.mp4'),
        ('All files', '*.*')
    )

    global current_file

    current_file = fd.askopenfilename(
        title = 'Open a file',
        initialdir = 'files/',
        filetypes=filetypes
    )

    print(type(current_file))
    text.set("Current File: \n" + current_file)

open_button = tk.Button(
    root, 
    text = 'Open a File',
    command=select_files
)

label.pack(ipadx=10, ipady=10)
open_button.pack(expand=True)
run_button.pack(expand=True)

root.mainloop()