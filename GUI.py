# Game GUI
import json
from tkinter import *
import random
from Game import check_word
import math

# Read in wordle_duden
with open("wordle_duden.json", "r") as duden:
    wordle_duden = json.load(duden)

# guess number
guess_numb = 0

# hits
hits = 0

# points
points_1 = 0

points_2 = 0

#points_dict
points_dict = {0: 6,
               1: 5,
               2: 4,
               3: 3,
               4: 2,
               5: 1}

# mess label
mess_label = 0

# player
player = 1

# round
iter = 1

# seed
randint = random.randrange(0, 1000)

# root anlegen
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

score_label_1 = Label(root, text=points_1, font=("Times 40"), bg="#333333", width = 2, height=1)
score_label_1.grid(row=3, column=1)

# Player 2
player_label_1 = Label(root, text="Spieler 2", font=("Times 40"), bg="#333333", width = 8, height=1)
player_label_1.grid(row=2, column=8)

score_label_2 = Label(root, text=points_2, font=("Times 40"), bg="#333333", width = 2, height=1)
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

# call check_word()
def enter_word():
    print("pressed")
    row_chars = []
    color_dict = {2: "darkgreen",
                  1: "gold",
                  0: "darkred"}

    # guess numb is a global variable
    global guess_numb
    global hits
    global points_1
    global points_2
    global mess_label
    global player
    global iter
    global randint

    # go to next word and delete entry text
    if hits == [2, 2, 2, 2, 2] or guess_numb == 6:
        # state normal again
        [x.configure(state="normal") for x in Entry_list]

        # delete text
        [x.delete(0, "end") for x in Entry_list]

        # reset label color
        for l in Label_list:
            l.configure({"fg": "white"})

        # new random seed
        randint = random.randrange(0, 1000)

        # stop the game after 5 Rounds
        if iter != 1.5:
            # add to round
            iter += 0.5

            # show round
            iter_label.config(text=math.floor(iter))

            # if the guess was correct
            if hits == [2, 2, 2, 2, 2]:

                # add points for the player
                if player == 1:
                    # calculate points
                    points_1 += points_dict[(guess_numb-1)]

                    #show points
                    score_label_1.config(text = points_1)

                    # next player
                    player = 2
                else:
                    # calculate points
                    points_2 += points_dict[(guess_numb-1)]

                    #show points
                    score_label_2.config(text = points_2)

                    # next player
                    player = 1
        else:
            # clear canvas
            for element in root.winfo_children():
                element.destroy()
            # Print the result
            end_label = Label(root, text=f'Ergebnis: {points_1}:{points_2}', font=("Times 40"), bg="#333333", width=8, height=1)
            end_label.pack(anchor="center")

            # show result


        # reset hits and guess_numb
        hits = 0
        guess_numb = 0

        # delete message label
        mess_label.destroy()

    # check if there are guesses left
    if guess_numb <= 5:
        # iterate through every entry object in row
        for l in range(0, 5):
            # if entry is not empty
            if Entry_list[guess_numb * 5 + l].get() != "":
                # append char
                row_chars.append(Entry_list[guess_numb * 5 + l].get())

        # if every char in row is filled
        if len(row_chars) == 5 and "".join(row_chars) in wordle_duden:
            # check word with current row
            hits, goal_word = check_word(word = "".join(row_chars), randint=randint, duden=wordle_duden)

            # color entrys and letters
            for k in range(0, len(row_chars)):
                Entry_list[guess_numb * 5 + k].configure(state = "disabled")
                Entry_list[guess_numb * 5 + k].configure({"disabledbackground": color_dict[hits[k]]})
                # letter color
                for l in Label_list:
                    if l["text"] == Entry_list[guess_numb * 5 + k].get():
                        l.configure({"fg":color_dict[hits[k]]})


            # if the correct word is guessed
            if hits == [2, 2, 2, 2, 2]:
                # print message
                mess_label = Label(root, text="Korrekt!", font=("Times 40"), bg="#333333", width=8, height=1)
                mess_label.grid(row=7, column=4)

            # if the word is wrong and its the last try
            elif guess_numb == 5:
                # print the word
                mess_label = Label(root, text=f'Falsch! Das Wort ist: {goal_word}', font=("Times 40"), bg="#333333", width=30, height=1)
                mess_label.grid(row=7, column=4)

            # if the word is wrong
            else:
                # print fail message
                mess_label = Label(root, text="Falsch!", font=("Times 40"), bg="#333333", width=8, height=1)
                mess_label.grid(row=7, column=4)

            print(hits)
            # add to guess_numb

            guess_numb += 1
            print(guess_numb)

    return guess_numb

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
button_entry = Button(root, text="Guess", image= entry_image, borderwidth=0, bd = 0, command= enter_word).grid(row=6, column=4)


# Mainloop
root.mainloop()
