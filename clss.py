from func import *
from util import *
from functools import partial

class command():
    # 画像処理コマンドと対応するボタンオブジェクト、軽い説明
    def __init__(self, func):
        self.process = func
        self.button_list = None
        self.button_easy = None
        self.is_skip = False

    def __call__(self, img, *args):
        if self.is_skip:
            return img
        else:
            return self.process(img)

    def show_button_easy(self, app, x, y):
        self.button_easy = Button(app.root, text=u"", command=partial(self.button_easy_process, app))
        self.button_easy.place(x=x, y=y)

    def button_easy_process(self, app):
        app.commands = [command(self.process)]
        app.output_image = process_all(app.input_image, app.commands)
        app.set_output_image()

class button():
    def __init__(self):
        pass

class button_list():
    # コマンドを一覧表示するほうのボタン
    def __init__(self):
        pass

class button_proc():
    # 画像処理コマンドの引数を指定する、入出力の型をわかりやすくするためのオブジェクト
    def __init__(self):
        pass