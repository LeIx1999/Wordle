# Game GUI
import json
from tkinter import *
import random
import math
import Game

# create an instance of the class Game
Game = Game.Game()

# create root
root = Tk()
root.title("Wordle")
root.geometry("1200x1200")

# set icon
root.iconbitmap("earth.ico")

# Game Title
Label(root, text = "WORDLE", font=("Times 50")).grid(row = 1, column=4)

# Scoreboard
# Player 1
player_label_1 = Label(root, text="Spieler 1", font=("Times 40"), bg="#333333", width = 8, height=1)
player_label_1.grid(row=2, column=1)

score_label_1 = Label(root, text=Game.points_1, font=("Times 40"), bg="#333333", width = 2, height=1)
score_label_1.grid(row=3, column=1)

# Player 2
player_label_1 = Label(root, text="Spieler 2", font=("Times 40"), bg="#333333", width = 8, height=1)
player_label_1.grid(row=2, column=8)

score_label_2 = Label(root, text=Game.points_2, font=("Times 40"), bg="#333333", width = 2, height=1)
score_label_2.grid(row=3, column=8)

# Round
iter_label = Label(root, text=f'Runde: {iter}', font=("Times 40"), bg="#333333", width = 8, height=1)
iter_label.grid(row=2, column=4)

# Mainframe
main_frame = Frame(root, padx=50, pady=50)
main_frame.grid(row=4, column=4)

# Secondframe
second_frame = Frame(root, padx=100, pady=100)
second_frame.grid(row=5, column=4)

# Make sure only one letter is entered
def validate_characters(chars):
    if len(chars) >1:
        return False
    else:
        return True

letter_cmd = (root.register(validate_characters), '%P')

# Entrys for letters
row = 0
column_list = [0, 1, 2, 3, 4] * 6
Entry_list = []
for i in range(0, 30):
    entry = Entry(main_frame, width = 4, font=("", 40), validate="key",
                  validatecommand=letter_cmd)

    # To call a function when Return is pressed
    #entry.bind('<Return>', enter_word(0))

    entry.grid(row=int(i / 5), column=column_list[i])
    Entry_list.append(entry)



# alphabet labels
letters_list = ["q", "w", "e", "r", "t", "z", "u", "i", "o", "p", "ü", "a", "s", "d",
                "f", "g", "h", "j", "k", "l", "ö", "ä", "y", "x", "c", "v", "b", "n", "m"]
column_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 2
column_list = column_list + [2 ,3, 4, 5, 6, 7, 8]
Label_list = []
for i in range(0, 29):
    label = Label(second_frame, text=letters_list[i], font=("Times 40"), bg="#333333", width = 1, height=1)

    label.grid(row=int(i/11), column= column_list[i])
    Label_list.append(label)

# button Image
entry_image = PhotoImage(file="icons8-button-91.png")
entry_label = Label(image=entry_image)

# Entry button
button_entry = Button(root, text="Guess", image= entry_image, borderwidth=0, bd = 0, command= lambda: Game.enter_word(Entry_list,
                        Label_list, iter_label, score_label_1, score_label_2, root)).grid(row=6, column=4)

# Mainloop
root.mainloop()
