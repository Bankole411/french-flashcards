from tkinter import *
import pandas as pd
import random

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")
# print(words_to_learn)

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}


def next_card():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(words_to_learn)
    canvas.itemconfig(card_image, image=card_front_image)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_word["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_word["English"], fill="white")
    canvas.itemconfig(card_image, image=card_back_image)


def known_word():
    words_to_learn.remove(current_word)
    next_card()
    data = pd.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)


window = Tk()
window.title("Bankole's Flashcard game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)


canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_image)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 300, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

tick_image = PhotoImage(file="images/right.png")
is_known = Button(image=tick_image, highlightthickness=0, command=known_word)
is_known.grid(row=1, column=1)

cross_image = PhotoImage(file="images/wrong.png")
not_known = Button(image=cross_image, highlightthickness=0, command=next_card)
not_known.grid(row=1, column=0)

next_card()


window.mainloop()
