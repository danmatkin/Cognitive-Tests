import time
import os.path
import sys
from tkinter import *
from tkmacosx import *
# from PIL import Image, ImageTk
# from PIL.Image import Resampling
import glob
import shutil
import random

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width/2.5)
window_height = int(screen_height/2.5)

# window_width = screen_width
# window_height = screen_height

window_area = window_width*window_height

image_height  = int(window_height/2.5)

root.geometry(f'{window_width}x{window_height}+{int(screen_height/1)}+0')

try:
    image_list = []
    path = '/Users/Work/PycharmProjects/HereGoes/ComicsNew'

    if not os.path.exists(path):
        os.makedirs(path)
        for filename in glob.glob('/CMIT_Comics/*.jpg'):
            image = Image.open(filename)
            width_height = image.size
            width_old = width_height[0]
            height_old = width_height[1]
            width_new = (image_height * width_old)/height_old
            image_resized = image.resize((int(width_new),int(image_height)), Image.LANCZOS)
            images = image_resized.save('{}{}{}'.format(path,'/',os.path.split(filename)[1]))

    for file in sorted(glob.glob('/Users/Work/PycharmProjects/HereGoes/ComicsNew/*jpg')):
        images = ImageTk.PhotoImage(Image.open(file))
        image_list.append(images)

    print(image_list)

    shutil.rmtree('ComicsNew')
except:
    pass

master_trial_outcomes = []
intra_trial_outcomes = []
master_level = 2
# titration = True
# spatial = False
# visual = False
# dual_task = False

class CumulativeMatrixTask:

    def __init__(self, window, level):
        self.level = level
        self.canvas = Canvas(window, width=window_width+10, height=window_height+10, highlightthickness=0)
        self.canvas.pack()
        self.label = Label(self.canvas, font=('Arial', 20))
        self.enclosing_frame = Frame(self.canvas, highlightthickness=1, highlightbackground="black")
        self.start_button = Button(window, text='Start', command=self.create_blocks) # Todo routine starts here
        self.start_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.submit_button = Button(self.canvas, text='Submit', command=self.submit)
        self.block_list = []
        self.blocks_needed = self.level * 2
        for x in range(self.blocks_needed):
            self.blocks = Button(self.enclosing_frame, width=int(window_width*0.05), height=int(window_width*0.05), bg='#ffffff', highlightthickness=4, focuscolor='')
            self.blocks.config(command=lambda x=self.blocks: self.colour_change(x))
            self.block_list.append(self.blocks)
        self.modulo = 2
        if int(self.level) in [x for x in range(3, 6)]:
            self.modulo = 3
        elif int(self.level) in [x for x in range(6, 9)]:
            self.modulo = 4
        elif int(self.level) in [x for x in range(9, 12)]:
            self.modulo = 5
        elif int(self.level) in [x for x in range(12, 15)]:
            self.modulo = 6
        x, y = 0, 0
        for block in self.block_list:
            if self.block_list.index(block) % self.modulo == 0:
                y = 0
                x += 1
            block.grid(row=x, column=y)
            y += 1

    def create_blocks(self):
        self.enclosing_frame.place(relx=.5, rely=.5, anchor=CENTER)
        self.start_button.destroy()
        root.after(2000, self.flash_routine)

    def colour_change(self, index):
        print(index)
        if index['bg'] == '#ffffff':
            index['bg'] = 'black'
            index['highlightbackground'] = 'black'
        elif index['bg'] == 'black':
            index['bg'] = '#ffffff'
            index['highlightbackground'] = '#ffffff'
        root.focus_set()

    def flash_routine(self):
        random.shuffle(self.block_list)
        self.flash_list = [x for x in self.block_list if self.block_list.index(x) < self.level]
        print(self.flash_list)
        for block in self.flash_list:
            print(block)
            block.config(bg='black', highlightbackground='black')
            root.update()
            time.sleep(1.5)
            block.config(bg='#ffffff', highlightbackground='#ffffff')
            root.update()
            time.sleep(0.5)
        root.after(1000, self.instructions)

    def instructions(self):
        self.enclosing_frame.place_forget()
        self.label.config(text='+')
        self.label.place(relx=.5, rely=.5, anchor=CENTER)
        root.update()
        root.after(2000, self.response)

    def response(self):
        self.enclosing_frame.place(relx=.5, rely=.5, anchor=CENTER)
        self.label.place_forget()
        self.submit_button.place(relx=.5, rely=.8, anchor=CENTER)
        root.update()

    def submit(self):
        global master_level, intra_trial_outcomes, master_trial_outcomes
        self.check_list = []
        for block in self.block_list:
            if block['bg'] == 'black':
                self.check_list.append(block)
        if self.check_list == self.flash_list:
            intra_trial_outcomes.append(1)
            if len(intra_trial_outcomes) == 2 and sum(intra_trial_outcomes) == 2 or sum(intra_trial_outcomes) == 3:
                master_trial_outcomes.append(intra_trial_outcomes[:])
                master_level += 1
                intra_trial_outcomes.clear()
                print(master_trial_outcomes)
        else:
            intra_trial_outcomes.append(0)
            if intra_trial_outcomes.count(0) == 3:
                master_trial_outcomes.append(intra_trial_outcomes[:])
                quit() # Todo use self.level here to set the experimental routines.

        self.canvas.destroy()
        CumulativeMatrixTask(root, master_level)

CumulativeMatrixTask(root, master_level)
root.mainloop()
