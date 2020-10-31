import sys, os
import tkinter as tk
from tkinter import Canvas, Button, StringVar, ttk, filedialog, messagebox
from PIL import Image, ImageTk
from clss import *
from func import *
from util import *
import params
import cv2
from functools import partial

class Application(tk.Frame):
    filepath = None
    commands = []
    input_canvas = None
    output_canvas = None
    input_image = None
    output_image = None
    input_thumbnail = None
    output_thumbnail = None

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.master.title('pic100-gui')
        self.root.geometry(params.root_geometry_size)

        #　入力ファイル画像表示の場所指定とサイズ指定
        self.input_canvas = Canvas(self.root, width=params.input_thumbnail_width, height=params.input_thumbnail_height)
        self.input_canvas.place(x=params.input_thumbnail_x, y=params.input_thumbnail_y)
        self.input_canvas["bg"] = "#05B3FF"
        # 出力ファイル画像表示の場所指定とサイズ指定
        self.output_canvas = Canvas(self.root, width=params.output_thumbnail_width, height=params.output_thumbnail_height)
        self.output_canvas.place(x=params.output_thumbnail_x, y=params.output_thumbnail_y)
        self.output_canvas["bg"] = "#05B3FF"

        # 参照ファイルパス表示ラベルの作成
        self.file1 = StringVar()
        self.file1_entry = ttk.Entry(self.root, textvariable=self.file1, width=70)
        self.file1_entry.grid(row=0, column=0, padx=20)

        # 参照ボタン配置
        button1 = Button(self.root, text=u'参照', command=self.button1_clicked)
        button1.grid(row=0, column=1, padx=10)

        # 閉じるボタン
        close1 = Button(self.root, text=u'閉じる', command=self.close_clicked)
        close1.grid(row=0,column=2)

        ##################################### # easy button仮置き
        self.btns = []
        self.btn_funcs = [BGR2RGB, BGR2GRAY, binarization, OTSU_binarization, hue_inversion, color_reduction, mean_pooling, max_pooling, Gaussian_filter, Median_filter]
        self.btn_commands = [command(i) for i in self.btn_funcs]
        for i, com in enumerate(self.btn_commands):
            com.show_button_easy(self, x=i*20, y=440)
        #######################################

    def set_input_image(self): # self.input_imageをresizeしてself.input_thumbnailに反映
        in_shape = self.input_image.shape
        in_rate = min(params.input_thumbnail_width/in_shape[1], params.input_thumbnail_height/in_shape[0])
        in_shape = (int(in_shape[1]*in_rate), int(in_shape[0]*in_rate))
        self.input_thumbnail = cv2.resize(self.input_image, dsize=in_shape)
        self.input_canvas.photo = ImageTk.PhotoImage(image=Image.fromarray(self.input_thumbnail))
        self.input_canvas.create_image(in_shape[0]//2, in_shape[1]//2, image=self.input_canvas.photo)


    def set_output_image(self): # self.output_imageをresizeしてself.output_thumbnailに反映
        out_shape = self.output_image.shape
        out_rate = min(params.output_thumbnail_width/out_shape[1], params.output_thumbnail_height/out_shape[0])
        out_shape = (int(out_shape[1]*out_rate), int(out_shape[0]*out_rate))
        self.output_thumbnail = cv2.resize(self.output_image, dsize=out_shape)
        self.output_canvas.photo = ImageTk.PhotoImage(image=Image.fromarray(self.output_thumbnail))
        self.output_canvas.create_image(out_shape[0]//2, out_shape[1]//2, image=self.output_canvas.photo)


    def button1_clicked(self):
        # 入力ファイル指定
        fTyp = [("画像ファイル", "*.jpeg"), ("画像ファイル", "*.jpg")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if self.filepath == "":
            return
        self.file1.set(self.filepath)

        # 画像ファイル読み込み
        self.input_image = BGR2RGB(cv2.imread(self.filepath))
        self.set_input_image()
        
        # 出力画像を作成(commandsに何も登録されていないときは元画像をそのまま出力するはず)
        self.output_image = process_all(self.input_image, self.commands)
        self.set_output_image()


    def close_clicked(self):
        res = messagebox.askokcancel("確認", "アプリを終了しますか？")
        if res != True:
            return
        sys.exit()