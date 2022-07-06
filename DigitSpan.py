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

class DigitSpanTest:

    def __init__(self, window):
        self.canvas = Canvas(window, width=window_width + 10, height=window_height + 10, highlightthickness=0)
        self.canvas.pack()
        self.intra_trial_outcomes = []
        self.level = 3
        self.isc_time = 3000

    def begin(self):
        self.start_button = Button(self.canvas, text='Start', command=self.interstimulus_cross)
        self.start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    def interstimulus_cross(self):
        self.start_button.destroy()
        self.label = Label(self.canvas, font=('Arial', 25), text='+')
        self.label.place(relx=.5, rely=.5, anchor=CENTER)
        root.after(self.isc_time, self.presentation_setup)

    def presentation_setup(self):
        self.digit_index = 0
        if self.level <= 9:
            self.digits = random.sample(range(10), self.level)
        else:
            self.digits = random.sample(range(99), self.level)
            while len(self.digits) != self.level:
                self.digits.pop()
        self.digits_display = '+'.join(map(str, self.digits))
        self.label.place(relx=.5, rely=.5, anchor=CENTER)
        for n in self.digits_display:
            self.label.config(text=f'{self.digits_display[self.digit_index]}')
            root.update()
            self.digit_index += 1
            time.sleep(1)
        root.after(0, self.instruction)

    def instruction(self):
        self.label.configure(text='[Instruction]')
        root.after(2000, self.response)

    def response(self):
        self.entry = Entry(self.canvas, justify='center', relief='sunken')
        self.entry.place(relx=.5, rely=.65, anchor=CENTER)
        self.entry.focus_set()
        self.entry.bind('<Return>', lambda x: self.response_check())

    def response_check(self):
        root.unbind_all('<Return>')
        self.digits_display = self.digits_display.replace('+', '')
        if self.entry.get() == self.digits_display:
            self.intra_trial_outcomes.append(1)
            if len(self.intra_trial_outcomes) == 2 and sum(self.intra_trial_outcomes) == 2 or sum(self.intra_trial_outcomes) == 3:
                master_trial_outcomes.append(self.intra_trial_outcomes[:])
                self.level += 1
                self.intra_trial_outcomes.clear()
        else:
            self.intra_trial_outcomes.append(0)
            if self.intra_trial_outcomes.count(0) == 3:
                master_trial_outcomes.append(self.intra_trial_outcomes[:])
        self.entry.destroy()
        self.label.destroy()
        self.begin()

start = DigitSpanTest(root)
start.begin()
root.mainloop()
