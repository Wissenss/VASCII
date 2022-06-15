import cv2
from PIL import Image, ImageOps
import os
import sys

ASCII_CHARS = ['@ ', '% ', '$ ', '# ', '* ', '+ ', '= ', '; ', ': ', ', ', '- ', '. ', '  ']

#source = Image.open(r"files/example_1.jpg")
source = cv2.VideoCapture("files/example_4.mp4")

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
            frame += ASCII_CHARS[pixels[width*i + j]//20]
        frame += "\n"
    sys.stdout.write(frame)

    #frame = "\n".join([line for line in ])
    return image

if isinstance(source, cv2.VideoCapture):
    while(source.isOpened()):
        ret, frame = source.read()
        image = Image.fromarray(frame)
        asciiImage(resizeGrayImage(image))
        if (not ret):
            break;
        cv2.imshow('video', frame)
        #cv2.waitKey(1)
        os.system("cls")
    source.release()
    cv2.destroyAllWindows()

