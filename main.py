import sys, os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  
from clss import *
from app import Application
import cv2

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()