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

class VisualPatternTest:

    def __init__(self, window):
        self.canvas = Canvas(window, width=window_width + 10, height=window_height + 10, highlightthickness=0)
        self.canvas.pack()
        self.intra_trial_outcomes = []
        self.level = 2
        self.isc_time = 2000

    def colour_change(self, index):
        if index['bg'] == '#ffffff':
            index['bg'] = 'black'
            index['highlightbackground'] = 'black'
        elif index['bg'] == 'black':
            index['bg'] = '#ffffff'
            index['highlightbackground'] = '#ffffff'
        root.focus_set()

    def begin(self):
        self.start_button = Button(self.canvas, text='Start', command=self.interstimulus_cross)
        self.start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    def interstimulus_cross(self):
        self.start_button.destroy()
        self.label = Label(self.canvas, font=('Arial', 25), text='+')
        self.label.place(relx=.5, rely=.5, anchor=CENTER)
        root.update()
        root.after(self.isc_time, self.block_setup)

    def block_setup(self):
        self.label.destroy()
        self.canvas2 = Canvas(self.canvas, width=window_width + 10, height=window_height + 10, highlightthickness=0)
        self.canvas2.pack()
        self.block_list = []
        self.block_frame_list = []
        self.enclosing_frame = Frame(self.canvas2, highlightthickness=0)
        for x in range(self.level*2):
            self.block_frames = Frame(self.enclosing_frame, highlightthickness=1, highlightbackground="gray")
            self.block_frame_list.append(self.block_frames)
            self.blocks = Button(self.block_frames, width=int(window_width*0.05), height=int(window_width*0.05), bg='#ffffff', highlightthickness=4, focuscolor='')
            self.blocks.config(command=lambda x=self.blocks: self.colour_change(x))
            self.block_list.append(self.blocks)
        self.modulo = 2
        if int(self.level) in [x for x in range(3, 5)]:
            self.modulo = 3
        elif int(self.level) in [x for x in range(5, 9)]:
            self.modulo = 4
        elif int(self.level) in [x for x in range(9, 12)]:
            self.modulo = 5
        elif int(self.level) in [x for x in range(12, 15)]:
            self.modulo = 6
        x, y = 0, 0
        for frame in self.block_frame_list:
            if self.block_frame_list.index(frame) % self.modulo == 0:
                y = 0
                x += 1
            frame.grid(row=x, column=y)
            y += 1
        for block in self.block_list:
            block.pack()
        self.enclosing_frame.place(relx=.5, rely=.5, anchor=CENTER)
        self.presentation()

    def presentation(self):
        random.shuffle(self.block_list)
        self.pattern_list = [x for x in self.block_list if self.block_list.index(x) < self.level]
        for block in self.pattern_list:
            block.config(bg='black', highlightbackground='black')
        root.after(2000, self.instruction)

    def instruction(self):
        self.enclosing_frame.place_forget()
        self.canvas3 = Canvas(self.canvas2, width=window_width + 10, height=window_height + 10, highlightthickness=0)
        self.canvas3.pack()
        self.label2 = Label(self.canvas3, text='[Instruction]', font=('Arial', 20))
        self.label2.place(relx=.5, rely=.5, anchor=CENTER)
        for block in self.pattern_list:
            block.config(bg='#ffffff', highlightbackground='#ffffff')
        root.after(2000, self.response)

    def response(self):
        self.label2.destroy()
        root.update()
        self.canvas3.destroy()
        self.enclosing_frame.place(relx=.5, rely=.5, anchor=CENTER)
        self.submit_button = Button(self.canvas2, text='Submit', command=self.submit)
        self.submit_button.place(relx=.5, rely=.75, anchor=CENTER)

    def submit(self):
        self.check_list = [block for block in self.block_list if block['bg']=='black']
        self.canvas2.destroy()
        if self.check_list == self.pattern_list:
            self.intra_trial_outcomes.append(1)
            if len(self.intra_trial_outcomes) == 2 and sum(self.intra_trial_outcomes) == 2 or sum(self.intra_trial_outcomes) == 3:
                master_trial_outcomes.append(self.intra_trial_outcomes[:])
                self.level += 1
                self.intra_trial_outcomes.clear()
        else:
            self.intra_trial_outcomes.append(0)
            if self.intra_trial_outcomes.count(0) == 3:
                master_trial_outcomes.append(self.intra_trial_outcomes[:])
        self.begin()

start = VisualPatternTest(root)
start.begin()
root.mainloop()
