"""Basic Visual Language Fluency Index script - This supposedly measures 'visual language fluency' but actually is just
generally a useful tool for assessing people's experience with comics."""

from tkinter import *
from tkmacosx import *

root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width/2)
window_height = int(screen_width/2)

window_area = window_width*window_height

root.geometry(f'{window_width}x{window_height}+{int(screen_height/1)}+0')
  # 7  # 15
q_set = [['On average, how often per week do you read text-only books for enjoyment?',  # 0
                 'On average, how often per week do you watch films?',  # 1
                 'On average, how often per week do you watch cartoons/anime?',  # 2
                 'On average, how often per week do you read comic books?',  # 3
                 'On average, how often per week do you read comic strips?',  # 4
                 'On average, how often per week do you read graphic novels?',  # 5
                 'On average, how often per week do you read Japanese comics (manga)?',  # 6
                 'On average, how often per week do you draw comics?'], ['On average, how often per week did you read text-only books for enjoyment while growing up?',  # 8
              'On average, how often per week did you watch films while growing up?',  # 9
              'On average, how often per week did you watch cartoons/anime while growing up?',  # 10
              'On average, how often per week did you read comic books while growing up?',  # 11
              'On average, how often per week did you read comic strips while growing up?',  # 12
              'On average, how often per week did you read graphic novels while growing up?',  # 13
              'On average, how often per week did you read Japanese comics (manga) while growing up?',  # 14
              'On average, how often per week did you draw comics while growing up?'], ['How would you currently rate your expertise with reading comics (of any sort)?',  # 16
                'How would you currently rate your drawing ability?', 'How would you rate your expertise with reading comics (of any sort) while growing up?',  # 18
             'How would you rate your drawing ability while growing up?']]
r_set = [[('1', 1),
      ('2', 2),
      ('3', 3),
      ('4', 4),
      ('5', 5),
      ('6', 6),
      ('7', 7)], [('1', 1),
      ('2', 2),
      ('3', 3),
      ('4', 4),
      ('5', 5)]]
e_set = ['Approximately how old were you when you first read a comic?',
             'Approximately how old were you when you first started drawing comics? (0 = N/A or Never)']

responses = []
rc = []

class VisualLanguageFluencyIndex:

    def __init__(self, window):
        self.canvas = Canvas(window, width=window_width + 10, height=window_height + 10, highlightthickness=0)
        self.canvas.pack()
        self.q_set_i = 0
        self.r_set_i = 0

    def start(self):
        self.start_button = Button(self.canvas, text='Start', command=self.questions)
        self.start_button.place(relx=.5, rely=.5, anchor=CENTER)

    def questions(self):
        self.start_button.destroy()
        self.q_l = []
        self.question_canvas = Canvas(self.canvas, highlightthickness=0, borderwidth=0)
        self.values = [IntVar() for i in range(len(q_set[self.q_set_i]))]
        self.i = 0
        for n in q_set[self.q_set_i]:
            self.question_rdb_canvas = Canvas(self.question_canvas)
            self.label = Label(self.question_canvas, text = n)
            self.label.pack()
            self.q_l.append(self.label)
            for t, v in r_set[self.r_set_i]:
                self.rdb = Radiobutton(self.question_rdb_canvas, text=t, val=v, variable=self.values[self.i]).pack(side=LEFT)
            self.question_rdb_canvas.pack()
            self.i += 1
        self.submit_button = Button(self.question_canvas, text='Submit', command=self.submit).pack()
        self.question_canvas.place(relx=.5, rely=.5, anchor=CENTER)

    def entry_questions(self):
        self.i = 0
        self.age_options = [x for x in range(0, 66)]
        self.values = [IntVar() for x in range(len(e_set))]
        self.question_canvas = Canvas(self.canvas, highlightthickness=0, borderwidth=0)
        for n in e_set:
            self.question_rdb_canvas = Canvas(self.question_canvas)
            self.ages = OptionMenu(self.question_canvas, self.values[self.i], *self.age_options)
            self.label = Label(self.question_canvas, text=n)
            self.label.pack()
            self.ages.pack()
            self.i += 1
        self.question_canvas.place(relx=.5, rely=.5, anchor=CENTER)
        self.submit_button = Button(self.question_canvas, text='Submit', command=self.submit).pack()

    def submit(self):
        self.rc = [x.get() for x in self.values]
        if len(responses) < 20 and 0 in self.rc:
            self.indices = [i for i, x in enumerate(self.rc) if x == 0]
            for n in self.indices:
                self.q_l[n].configure(fg='red')
                self.canvas.update()
        elif len(responses) != 20: # This is the point that needs to change
            self.question_canvas.destroy()
            responses.extend(self.rc)
            self.q_set_i += 1
            if self.q_set_i > 2:
                self.entry_questions()
            elif self.q_set_i < 2:
                self.questions()
            elif self.q_set_i == 2:
                self.r_set_i += 1
                self.questions()
        else:
            responses.extend(self.rc)
            self.calculate()

    def calculate(self):
        self.question_canvas.destroy()
        self.a = sum(responses[3:7])/4
        self.b = sum(responses[10:14])/4
        self.c = self.a*responses[16]
        self.d = self.b*responses[18]
        self.e = (self.c+self.d)/2
        self.f = (responses[7] + responses[15])/2
        self.g = (responses[17] + responses[19])/2
        self.h = self.f*self.g/2
        self.vlfi_score = self.e+self.h
        self.label = Label(self.canvas, text = f'{self.vlfi_score}')
        self.label.place(relx=.5, rely=.5, anchor=CENTER)

start=VisualLanguageFluencyIndex(root)
start.start()

root.mainloop()
