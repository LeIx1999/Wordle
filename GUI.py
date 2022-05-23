# Game GUI
import json
from tkinter import *
import random
from Game import check_word

# Read in wordle_duden
with open("wordle_duden.json", "r") as duden:
    wordle_duden = json.load(duden)

# guess number
guess_numb = 0

# hits
hits = 0

# root anlegen
root = Tk()
root.title("Wordle")
root.geometry("1200x1200")

# set icon
root.iconbitmap("earth.ico")

# Game Title
Label(root, text = "WORDLE", font=("Times 50")).pack(anchor="n")

# Mainframe
main_frame = Frame(root, padx=50, pady=50)
main_frame.pack()


# Secondframe
second_frame = Frame(root, padx=100, pady=100)
second_frame.pack()

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

    # go to next word and delete entry text
    if hits == [2, 2, 2, 2, 2]:
        # state normal again
        [x.configure(state="normal") for x in Entry_list]
        # delete text
        [x.delete(0, "end") for x in Entry_list]
        hits = 0
    # check if there are guesses left
    if guess_numb < 5:
        # iterate through every entry object in row
        for l in range(0, 5):
            # if entry is not empty
            if Entry_list[guess_numb * 5 + l].get() != "":
                # append char
                row_chars.append(Entry_list[guess_numb * 5 + l].get())

        # if every char in row is filled
        if len(row_chars) == 5:
            # check word with current row
            hits = check_word(word = "".join(row_chars), seed=3, duden=wordle_duden)
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
                Label(root, text="Korrekt!", font=("Times 40"), bg="#333333", width=8, height=1).pack(anchor="s")

            print(hits)
            # add to guess_numb

            guess_numb = + 1
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
button_entry = Button(root, text="Guess", image= entry_image, borderwidth=0, bd = 0, command= enter_word).pack(anchor="s")

# Mainloop
root.mainloop()