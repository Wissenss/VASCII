from ssl import Options
from turtle import bgcolor
import cv2
from PIL import Image, ImageOps
import os
import sys
import tkinter as tk
from tkinter import StringVar, filedialog as fd

class Txt_file():
    def __init__(self):
        self.CHARS = ['@ ', '% ', '$ ', '# ', '* ', '+ ', '= ', '; ', ': ', ', ', '- ', '. ', '  ']
        self.palete = len(self.CHARS)
        self.invert = False

    def resizeGrayImage(self, image, newWidth=70):
        width, height = image.size
        ratio = height/width
        newHeight = int(ratio*newWidth)
        image = ImageOps.grayscale(image.resize((newWidth, newHeight)))
        return image

    def asciiImage(self, image):
        width, height = image.size
        pixels = list(image.getdata())

        frame = ""
        for i in range(height):
            for j in range(width):
                if(self.invert):
                    frame += self.CHARS[pixels[width*i + j]//20]
                else:
                    frame += self.CHARS[len(self.CHARS)-(pixels[width*i + j]//20)-1]
            frame += "\n"
        frame += "\n\n"
        sys.stdout.write(frame)

        #frame = "\n".join([line for line in ])
        return image

    def execute_txt(self, filename):
        name, extention = os.path.splitext(str(filename))

        if extention == ".mp4":
            source = cv2.VideoCapture(filename)

            while(source.isOpened()):
                ret, frame = source.read()
                try:
                    image = Image.fromarray(frame)
                except AttributeError:
                    source.release()
                    cv2.destroyAllWindows()
                self.asciiImage(self.resizeGrayImage(image))
                if not ret:
                    break
                cv2.waitKey(10)
                cv2.imshow('video', frame)
        elif extention == ".jpg":
            source = Image.open(r"files/example_1.jpg")
            
            self.asciiImage(self.resizeGrayImage(source))
        else:
            return

root = tk.Tk()

class App(Txt_file):
    def __init__(self):
        super().__init__()
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

        #set window background color
        root.configure(bg='black')

        #set window icon
        root.iconbitmap('assets/icon.ico')

        #Main storage
        self.current_file = ""
        self.text = StringVar()
        self.bgColor = StringVar()

        self.text.set("Select a File!")

        frame = tk.Frame(root, bg='black')
        frame.place(relx =.5, rely=.5, anchor="center")

        title = tk.Frame(frame, width=40, height=40, bg = 'blue')
        title.grid(column=1, row=0)

        options = tk.Frame(frame, bg='black')
        options.grid(column=1, row=1)

        #GUI
        label = tk.Label(
            title, 
            bg = 'black',
            fg = 'white',
            textvariable=self.text
            )

        open_button = tk.Button(
            options, 
            text = 'Open a File',
            bg = 'black',
            fg = 'white',
            command=self.select_files,
            activebackground="gray",
            padx=5,
            pady=5,
            height=5,
            width=20
            )

        self.invert_button = tk.Button(
            options,
            text = 'Invert',
            bg='black',
            fg = 'white',
            command = self.invert_image,
            activebackground="gray",
            padx=5,
            pady=5,
            height=5,
            width=20
        )

        self.run_button = tk.Button(
            options, 
            text = 'Load',
            bg = 'black',
            fg = 'white',
            command=self.run,
            #activebackground="gray",
            highlightcolor='blue',
            padx=5,
            pady=5,
            height=5,
            width=20,
            state='disabled'
            )

        label.grid(column=0, row=0, columnspan=2)
        open_button.grid(column=0, row=1)
        self.invert_button.grid(column=1, row=1)
        self.run_button.grid(column=0, row=2)

    def invert_image(self):
        if self.invert == False:
            self.invert_button.configure(bg='white', fg='black')
            self.invert = True
        else:
            self.invert_button.configure(bg='black', fg='white')
            self.invert = False
        

    def select_files(self):
        filetypes = (
        ('video files', '*.mp4'),
        ('image files', '*.jpg'),
        ('All files', '*.*')
        )

        self.current_file = fd.askopenfilename(
            title = 'Open a file',
            initialdir = 'files/',
            filetypes=filetypes
        )

        if(self.current_file==""):
            self.run_button.configure(state='disabled')
            self.text.set("Select a File!")

        else:
            self.run_button.configure(state='active')
            name, extention = os.path.splitext(str(self.current_file))
            name = name.split('/')[-1]
            self.text.set("Current File: " + name + extention)

    def run(self):
        self.execute_txt(self.current_file)

App()
root.mainloop()