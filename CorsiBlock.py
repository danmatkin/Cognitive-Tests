import time
import os.path
import sys
from tkinter import *
from tkmacosx import *
from PIL import Image, ImageTk
from PIL.Image import Resampling
import glob
import shutil
import random

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width/2.5)
window_height = int(screen_height/2.5)

window_area = window_width*window_height

image_height  = int(window_height/2.5)

root.geometry(f'{window_width}x{window_height}+{int(screen_height/1)}+0')

master_trial_outcomes = []

class CorsiBlockTest:

    def __init__(self, window):
        self.canvas = Canvas(window, width=window_width + 10, height=window_height + 10, highlightthickness=0)
        self.canvas.pack()
        self.intra_trial_outcomes = []
        self.level = 3
        self.block_list = []
        self.isc_time = 2000

    def click_block(self, block):
        if block['bg'] == 'black':
            self.response_list.append(block)
            block.config(text = f'{self.response_list.index(block)+1}', font=('Arial', 12))
            block['width']=int(window_width * 0.05)
            block['height']=int(window_width * 0.05)
            block['bg'] = 'red'
            root.update()
            print(self.response_list)
        elif block['bg'] == 'red':
            self.response_list.remove(block)
            block.config(text = '')
            block['bg']='black'
            block['width']=int(window_width * 0.05)
            block['height']=int(window_width * 0.05)
            root.update()
        root.focus_set()

    def begin(self):
        self.start_button = Button(self.canvas, text='Start', command=self.interstimulus_cross)
        self.start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    def interstimulus_cross(self):
        self.start_button.destroy()
        self.label = Label(self.canvas, font=('Arial', 25), text='+')
        self.label.place(relx=.5, rely=.5, anchor=CENTER)
        root.update()
        root.after(self.isc_time, self.presentation)

    def presentation(self):
        self.canvas2 = Canvas(self.canvas, width=window_width + 10, height=window_height + 10, highlightthickness=0)
        self.canvas2.pack()
        for x in range(0,9):
            self.blocks = Button(self.canvas2, width=int(window_width * 0.05), height=int(window_width * 0.05),
                                 bg='black', highlightthickness=4, focuscolor='', fg='black')
            self.blocks.config(command=lambda x=self.blocks: self.click_block(x))
            self.block_list.append(self.blocks)
        self.response_list = []
        self.label.destroy()
        self.flash_list = [x for x in self.block_list if self.block_list.index(x) < self.level]
        self.x = random.sample(range(9, 91, 10), 9)
        self.y = random.sample(range(9, 91, 10), 9)
        self.x_i = 0
        self.y_i = 0
        for block in self.block_list:
            block.place(relx=self.x[self.x_i]/100,rely=self.y[self.y_i]/100, anchor=CENTER)
            self.x_i += 1
            self.y_i += 1
        root.after(2000, self.flash_routine)

    def flash_routine(self):
        for block in self.flash_list:
            block.config(bg='red')
            root.update()
            time.sleep(1.5)
            block.config(bg='black')
            root.update()
            time.sleep(0.5)
        root.after(1000, self.instructions)

    def instructions(self):
        self.canvas3 = Canvas(self.canvas2, width=window_width + 10, height=window_height + 10, highlightthickness=0)
        self.canvas3.pack()
        self.label = Label(self.canvas3, text='[Instruction]', font=('Arial', 20))
        self.label.place(relx=.5, rely=.5, anchor=CENTER)
        root.after(2000, self.response)

    def response(self):
        self.canvas3.destroy()
        root.bind_all('<Return>', lambda x:self.response_check())

    def response_check(self):
        root.unbind_all('<Return>')
        if self.response_list == self.flash_list:
            self.intra_trial_outcomes.append(1)
            if len(self.intra_trial_outcomes) == 2 and sum(self.intra_trial_outcomes) == 2 or sum(self.intra_trial_outcomes) == 3:
                master_trial_outcomes.append(self.intra_trial_outcomes[:])
                self.level += 1
                self.intra_trial_outcomes.clear()
        else:
            self.intra_trial_outcomes.append(0)
            if self.intra_trial_outcomes.count(0) == 3:
                master_trial_outcomes.append(self.intra_trial_outcomes[:])
        self.block_list.clear()
        self.canvas2.destroy()
        self.begin()

start = CorsiBlockTest(root)
start.begin()
root.mainloop()
