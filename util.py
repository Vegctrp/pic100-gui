import sys, os
import tkinter as tk
from tkinter import Canvas, Button, StringVar, ttk, filedialog, messagebox
from PIL import Image, ImageTk
from clss import *
from func import *
import cv2
import numpy as np

def process_all(input_image, commands):
    image = input_image.copy()
    for com in commands:
        image = com(image).astype(np.uint8)
    return image