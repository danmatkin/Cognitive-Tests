from tkinter import *
from tkmacosx import *

root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width/2.5)
window_height = int(screen_height/2.5)

window_area = window_width*window_height

root.geometry(f'{window_width}x{window_height}+{int(screen_height/1)}+0')

instructions = ["Visual imagery refers to the ability to visualise, that is, the ability to form mental pictures, or to 'see in the minds eye'. Marked individual differences have been found in the strength and clarity of reported visual imagery and these differences are of considerable psychological interest.",
                "The aim of this test is to determine the vividness of your visual imagery. The items of the test will possibly bring certain images to your mind. You are asked to rate the vividness of each image by reference to the 5-point scale given below: No image at all, Vague and dim, Moderately clear and vivid, reasonably clear and vivid Perfectly clear & vivid as if I was actually seeing it.\n\nThroughout the test, refer to the rating scale when judging the vividness of each item separately, independent of how you may have done other items.",
                "For each question, you should read the item, shut your eyes, attempt to form a mental picture, then open your eyes and complete the rating scale."]

questions = [['In answering items 1 to 4, think of some relative or friend whom you frequently see and consider carefully the picture that comes your mind’s eye.', '1. The exact contour of face, head, shoulders and body.', '2. Characteristic poses of head, attitudes of body etc.', '3. The precise carriage, length of step, etc. in walking.', '4. The different colours worn in some familiar clothes.'],
             ['In answering item 5 to 8, think of the items mentioned in the following questions and rate the vividness of your imagination.','5. The sun is rising above the horizon into a hazy sky.','6. The sky clears and surrounds the sun with blueness.','7. Clouds. A storm blows up, with flashes of lighting.','8. A rainbow appears.'],
             ['In answering items 9 to 12, think of the front of a shop which you often go to. Consider the picture that comes before your mind’s eye.','9. The overall appearance of the shop from the opposite side of the road.','10. A window display including colours, shape and details of individual items for sale.','11. You are near the entrance. The colour, shape and details of the door.','12. You enter the shop and go to the counter. The counter assist serves you. Money changes hands.'],
             ['In answering items 13 to 16, think of a country scene which involves trees, mountains and a lake.','13. The contours of the landscape.','14. The colour and shape of the trees.', '15. The colour and shape of the lake.', '16. A strong wind blows on the trees and on the lake causing waves.'],
             ['In answering items 17 to 20, think of being driven in a fast-moving automobile by a relative or friend along a major highway. Consider the pictures that comes into your mind’s eye.', '17. You observe the heavy traffic travelling at maximum speed around your car. The overall appearance of vehicles, their colours, sizes and shapes.', '18. Your car accelerates to overtake the traffic directly in front of you. You see an urgent expression on the face of the driver and the people in the other vehicles as you pass.', '19. A large truck is flashing its headlights directly behind. Your car quickly moves over to let the truck pass. The driver signals with a friendly wave.', '20. You see a broken - down vehicle beside the road. Its lights are flashing. The driver is looking concerned and she is using a mobile phone.'],
             ['In answering items 21 to 24, think of a beach by the ocean on a warm summer’s day. Consider the picture that comes before you minds’ eye.','21. The overall appearance and colour of the water, surf, and sky.', '22. Bathers are swimming and splashing about in the water. Some are playing with a brightly coloured beach ball.', '23. An ocean liner crosses the horizon. It leaves a trail of smoke in the blue sky.', '24. A beautiful air balloon appears with four people aboard. The balloon drifts past you, almost directly overhead. The passengers wave and smile. You wave and smile back at them.'],
             ['In answering items 25 to 28, think of a railway station. Consider the picture that comes before you mind’s eye.','25. The overall appearance of the station viewed in front of the main entrance.','26. You walk into the station. The colour, shape and details of the entrance hall.','27. You approach the ticket office, go to a vacant counter and purchase your ticket.','28. You walk to the platform and observe other passengers and the railway lines. A train arrives. You climb aboard.'],
             ['Finally, in answering items 29 to 32, think of a garden with lawns, bushes, flowers and shrubs. Consider the picture that comes before your mind’s eye.', '29. The overall appearance and design of the garden.', '30. The colour and shape of the bushes and shrubs.', '31. The colour and appearance of the flowers.', '32. Some birds fly down onto the lawn and start pecking for food.']]

r_set = [('No image at all', 1),
         ('Vague and dim image',2),
         ('Moderately clear and vivid',3),
         ('Reasonably clear and Vivid',4),
         ('Perfectly clear and vivid',5)]

responses = []
rc = []

class VividnessOfVisualImageryQuestionnaire2:

    def __init__(self, window):
        self.canvas = Canvas(window, width=window_width + 10, height=window_height + 10, highlightthickness=0)
        self.canvas.pack()
        self.q_i = 0
        self.intra_q_i = 1
        self.i_i = 0

    def start(self):
        self.start_button = Button(self.canvas, text='Start', command=self.instructions)
        self.start_button.place(relx=.5, rely=.5, anchor=CENTER)

    def instructions(self):
        self.start_button.destroy()
        self.instruction_canvas = Canvas(self.canvas, highlightthickness=0, borderwidth=0)
        self.instruction_canvas.place(relx=.5,rely=.5,anchor=CENTER)
        self.label = Label(self.instruction_canvas, text=f'{instructions[self.i_i]}', justify=CENTER, wraplength=500)
        self.label.pack()
        self.next_button = Button(self.canvas, text='Next', command=self.next_i)
        self.prev_button = Button(self.canvas, text='Previous', command=self.prev_i)
        self.next_button.place(relx=.75, rely=.85, anchor=CENTER)

    def next_i(self):
        self.i_i += 1
        self.label.config(text=f'{instructions[self.i_i]}')
        if self.i_i >= 1:
            self.prev_button.place(relx=.25, rely=.85, anchor=CENTER)
        if self.i_i == 2:
            self.next_button.config(text='Start', command=self.title)
        root.update()

    def prev_i(self):
        self.i_i -= 1
        self.label.config(text=f'{instructions[self.i_i]}')
        if self.i_i < 1:
            self.prev_button.place_forget()
        if self.i_i < 2:
            self.next_button.config(text='Next', command=self.next_i)
        root.update()

    def title(self):
        self.prev_button.destroy()
        self.next_button.destroy()
        self.label.destroy()
        self.title_canvas = Canvas(self.canvas,highlightthickness=0, borderwidth=0)
        self.title_label = Label(self.title_canvas, text=f'{questions[self.q_i][0]}', wraplength=500, justify=CENTER)
        self.title_label.pack()
        self.button = Button(self.title_canvas, text='Next', command=self.questions)
        self.button.pack(pady=20)
        self.title_canvas.place(relx=.5, rely=.5, anchor=CENTER)

    def questions(self):
        self.question_canvas = Canvas(self.canvas, highlightthickness=0, borderwidth=0)
        self.question_canvas.place(relx=.5, rely=.5, anchor=CENTER)
        self.title_canvas.destroy()
        self.title_label = Label(self.question_canvas, text=f'{questions[self.q_i][0]}', wraplength=500, justify=CENTER)
        self.value = IntVar()
        self.title_label.pack(pady=15)
        self.question_label = Label(self.question_canvas, text=f'{questions[self.q_i][self.intra_q_i]}',wraplength=650, justify=CENTER)
        self.question_label.pack(pady=40)
        for t, v in r_set:
            self.rdb = Radiobutton(self.question_canvas, text=t, val=v, variable=self.value, justify=LEFT).pack()
        self.submit_button = Button(self.question_canvas, text='Next', command=self.next_q)
        self.submit_button.pack(pady=50)

    def next_q(self):
        if self.value.get() == 0:
            pass
        else:
            responses.append(self.value.get())
            self.question_canvas.destroy()
            if len(responses) == 32:
                print(sum(responses))
                quit()
            if self.intra_q_i % 4 == 0:
                self.q_i += 1
                self.intra_q_i = 1
                self.title()

            elif self.intra_q_i % 4 != 0:
                self.intra_q_i += 1
                self.questions()




start=VividnessOfVisualImageryQuestionnaire2(root)
start.start()

root.mainloop()