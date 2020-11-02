from func import *
from util import *
from tkinter import Button
from functools import partial

class command():
    # 画像処理コマンドと対応するボタンオブジェクト、軽い説明
    def __init__(self, func, app):
        self.process = func
        self.app = app
        self.is_skip = False

    def __call__(self, img, *args):
        if self.is_skip:
            return img
        else:
            return self.process(img, *args)
    
    def copy(self):
        return command(self.process, self.app)

class command_easy(command):
    def __init__(self, func, app):
        super().__init__(func, app)
    
    def show_button(self, x, y):
        self.button = button_easy(self.app, self, x, y)

    def button_process(self):
        self.app.commands = [command_proc(self.process.copy(), self.app)]
        self.app.process()

class command_list(command):
    def __init__(self, func, app):
        super().__init__(func, app)
    
    def show_button(self, x, y):
        self.button = button_list(self.app, self, x, y)

    def button_process(self):
        self.app.commands = [command_proc(self.process.copy(), self.app)]
        #self.app.commands.append(command(self.process.copy(), self.app))
        self.app.process()

class command_proc(command):
    def __init__(self, func, app):
        super().__init__(func, app)
    
    def show_button(self, x, y):
        self.button = button_proc(self.app, self, x, y)
    
    def button_process(self):
        pass



class button():
    def __init__(self, app, command, x, y):
        self.app = app
        self.command = command
        self.button = None
        self.make_button(x, y)
    
    def make_button(self, x, y):
        pass

class button_easy(button):
    def __init__(self, app, command, x, y):
        super().__init__(app, command, x, y)

    def make_button(self, x, y):
        self.button = Button(self.app.root, text=u"", command=self.command.button_process)
        self.button.place(x=x, y=y)

class button_list(button):
    # コマンドを一覧表示するほうのボタン
    def __init__(self, app, command, x, y):
        super().__init__(app, command, x, y)
    
    def make_button(self, x, y):
        self.button = Button(self.app.root, text=u"", command=self.command.button_process)
        self.button.place(x=x, y=y)

class button_proc(button):
    # 画像処理コマンドの引数を指定する、入出力の型をわかりやすくするためのオブジェクト
    def __init__(self, app, command, x, y):
        super().__init__(app, command, x, y)

    def make_button(self, x, y):
        pass