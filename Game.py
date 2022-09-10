import json
import random
import math
from tkinter import *

# Define class Game
class Game:
    def __init__(self) -> None:
        # Read in wordle_duden
        with open("wordle_duden.json", "r") as duden:
            self.wordle_duden = json.load(duden)
        # guess number
        self.guess_numb = 0
        # hits
        self.hits = 0
        # points
        self.points_1 = 0
        self.points_2 = 0
        #points_dict
        self.points_dict = {0: 6,
                    1: 5,
                    2: 4,
                    3: 3,
                    4: 2,
                    5: 1}
        # mess label
        self.mess_label = 0
        # player
        self.player = 1
        # round
        self.iter = 1
        # seed
        self.randint = random.randrange(0, 1000)
        # color dictionary
        self.color_dict = {2: "darkgreen",
                    1: "gold",
                    0: "darkred"}
    
    def enter_word(self, Entry_list, Label_list, iter_label, score_label_1, score_label_2, root):
        row_chars = []

        # go to next word and delete entry text
        if self.hits == [2, 2, 2, 2, 2] or self.guess_numb == 6:
            # state normal again
            [x.configure(state="normal") for x in Entry_list]

            # delete text
            [x.delete(0, "end") for x in Entry_list]

            # reset label color
            for l in Label_list:
                l.configure({"fg": "white"})

            # new random seed
            self.randint = random.randrange(0, 1000)

            # stop the game after 5 Rounds
            if self.iter != 5.5:
                # add to round
                self.iter += 0.5

                # show round
                iter_label.config(text=math.floor(self.iter))

                # if the guess was correct
                if self.hits == [2, 2, 2, 2, 2]:

                    # add points for the player
                    if self.player == 1:
                        # calculate points
                        self.points_1 += self.points_dict[(self.guess_numb-1)]

                        #show points
                        score_label_1.config(text = self.points_1)

                        # next player
                        self.player = 2
                    else:
                        # calculate points
                        self.points_2 += self.points_dict[(self.guess_numb-1)]

                        #show points
                        score_label_2.config(text = self.points_2)

                        # next player
                        self.player = 1
            else:
                # clear canvas
                for element in root.winfo_children():
                    element.destroy()
                # Print the result
                end_label = Label(root, text=f'Ergebnis: {self.points_1}:{self.points_2}', font=("Times 40"), bg="#333333", width=20, height=1)
                end_label.pack(anchor="center")

                # show result


            # reset hits and guess_numb
            self.hits = 0
            self.guess_numb = 0

            # delete message label
            mess_label.destroy()

        # check if there are guesses left
        if self.guess_numb <= 5:
            # iterate through every entry object in row
            for l in range(0, 5):
                # if entry is not empty
                if Entry_list[self.guess_numb * 5 + l].get() != "":
                    # append char
                    row_chars.append(Entry_list[self.guess_numb * 5 + l].get())
            # save word
            self.word = "".join(row_chars)

            # if every char in row is filled
            if len(row_chars) == 5 and "".join(row_chars) in self.wordle_duden:
                # check word with current row
                self.hits = self.check_word()

                # color entrys and letters
                for k in range(0, len(row_chars)):
                    Entry_list[self.guess_numb * 5 + k].configure(state = "disabled")
                    Entry_list[self.guess_numb * 5 + k].configure({"disabledbackground": self.color_dict[self.hits[k]]})
                    # letter color
                    for l in Label_list:
                        if l["text"] == Entry_list[self.guess_numb * 5 + k].get():
                            l.configure({"fg":self.color_dict[self.hits[k]]})


                # if the correct word is guessed
                if self.hits == [2, 2, 2, 2, 2]:
                    # print message
                    mess_label = Label(root, text="Korrekt!", font=("Times 40"), bg="#333333", width=8, height=1)
                    mess_label.grid(row=7, column=4)

                # if the word is wrong and its the last try
                elif self.guess_numb == 5:
                    # print the word
                    mess_label = Label(root, text=f'Falsch! Das Wort ist: {self.goal_word}', font=("Times 40"), bg="#333333", width=30, height=1)
                    mess_label.grid(row=7, column=4)

                # if the word is wrong
                else:
                    # print fail message
                    mess_label = Label(root, text="Falsch!", font=("Times 40"), bg="#333333", width=8, height=1)
                    mess_label.grid(row=7, column=4)

                print(self.hits)
                # add to guess_numb

                self.guess_numb += 1

        return self.guess_numb

    def check_word(self):
        occurrence_list = []

        # find goal word
        self.goal_word = self.wordle_duden[self.randint]

        for i in range(0, 5):
            # correct position and char
            if self.word[i] == self.goal_word[i]:
                occurrence_list.append(2)
            # correct char
            elif self.word[i] in self.goal_word:
                occurrence_list.append(1)
            else:
                occurrence_list.append(0)

        return occurrence_list
    
    