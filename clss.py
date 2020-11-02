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
        self.button = None

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
        self.app.commands = [command_proc(self.process.copy(), self.app, len(self.app.commands))]
        self.app.process()

class command_list(command):
    def __init__(self, func, app):
        super().__init__(func, app)
    
    def show_button(self, x, y):
        self.button = button_list(self.app, self, x, y)

    def button_process(self):
        #self.app.commands = [command_proc(self.process.copy(), self.app, len(self.app.commands))]
        self.app.commands.append(command_proc(self.process.copy(), self.app, len(self.app.commands)))
        self.app.process()
        self.app.set_proc_buttons()

class command_proc(command):
    def __init__(self, func, app, index):
        super().__init__(func, app)
        self.index = index
    
    def show_button(self, x, y):
        self.button = button_proc(self.app, self, x, y)
    
    #def button_process(self):
    #    pass

    def button_delete(self):
        #self.button.place_forget()
        #self.app.commands.pop(self.index)
        #self.app.process()
        self.app.delete_proc(self.index)




class button():
    def __init__(self, app, command, x, y):
        self.app = app
        self.command = command
        self.button = None
        self.x = x
        self.y = y
        self.make_button()
    
    def emplace_button(self):
        pass

    def make_button(self):
        pass

class button_easy(button):
    def __init__(self, app, command, x, y):
        super().__init__(app, command, x, y)

    def emplace_button(self):
        self.button.place(x=self.x, y=self.y)
    
    def make_button(self):
        self.button = Button(self.app.root, text=u"", command=self.command.button_process)
        self.emplace_button()

class button_list(button):
    # コマンドを一覧表示するほうのボタン
    def __init__(self, app, command, x, y):
        super().__init__(app, command, x, y)

    def emplace_button(self):
        self.button.place(x=self.x, y=self.y)

    def make_button(self):
        self.button = Button(self.app.root, text=self.command.process.name, command=self.command.button_process)
        self.emplace_button()

class button_proc(button):
    # 画像処理コマンドの引数を指定する、入出力の型をわかりやすくするためのオブジェクト
    def __init__(self, app, command, x, y):
        super().__init__(app, command, x, y)

    def emplace_button(self):
        self.button_delete.place(x=self.x, y=self.y)

    def make_button(self):
        self.button_delete = Button(self.app.root, text=self.command.process.name, command=self.command.button_delete)
        self.emplace_button()
    
    def destroy(self):
        self.button_delete.destroy()