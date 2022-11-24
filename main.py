from tkinter import *
import pandas
import random
# -------------------------------------------------- FUNCTIONS -------------------------------------------------- #
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/spanish_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=current_card["Spanish"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# --------------------------------------------------  UI SETUP -------------------------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("FLASHY")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 150, fill="black", font=("Ariel", 40, "italic"), text="Title")
card_word = canvas.create_text(400, 263, fill="black", font=("Ariel", 60, "bold"), text="word")


# Buttons
cross_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=cross_img, highlightthickness=0, bd=0, command=next_card)
wrong_button.grid(column=0, row=1)


check_img = PhotoImage(file="images/right.png")
right_button = Button(image=check_img, highlightthickness=0, bd=0, command=is_known)
right_button.grid(column=1, row=1)


next_card()


window.mainloop()
