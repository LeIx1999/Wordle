import json
import random
import math
from tkinter import *
import re
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
        # ineligible guess
        self.ineligible = False

    def enter_word(self, Entry_list: list, Label_list: list, iter_label: Label, score_label_1: Label, score_label_2: Label, player_label_1: Label, player_label_2: Label,root: Tk) -> int: 
        self.row_chars = []

        # clear mess_label if its the second guess or the guess before was ineligible
        if self.guess_numb != 0 or self.ineligible:
            self.mess_label.destroy()
            self.ineligible = False

        # check if the word was correct or there are no guesses left
        if self.hits == [2, 2, 2, 2, 2] or self.guess_numb == 6:
            # go to next word and delete entry text
            self._end_round(Entry_list, Label_list)
            
            # stop the game after 5 Rounds
            if self.iter != 5.5:
                self._calculate_points(iter_label, score_label_1, score_label_2)
            else:
                self._end_game(root)
            # reset hits and guess_numb
            self.hits = 0
            self.guess_numb = 0

            # delete message label
            self.mess_label.destroy()
              

        # check if there are guesses left
        else:
            # build a word out of every char in the Entry_list
            self._build_word(Entry_list)

            # if every char in row is filled
            if len(self.word) == 5 and self.word in self.wordle_duden:
                # check word with current row
                self.hits = self._check_word()

                # color entrys and labels
                self._color_entrys(Entry_list, Label_list)

                # show the evaluation of the word
                self._show_evaluation(root)
            
            elif len(self.word) == 5:
                # print that the word is not in the duden
                self.mess_label = Label(root, text=" Das Wort ist nicht zulässig!", font=("Times 40"), bg="#333333", width=30, height=1)
                self.mess_label.grid(row=7, column=4)
                self.ineligible = True


        # change the color of the player name
        self._change_player_color(player_label_1, player_label_2)

        return self.guess_numb               

    def _end_round(self, Entry_list: list, Label_list: list) -> None:
        # state normal again
        [x.configure(state="normal") for x in Entry_list]

        # delete text
        [x.delete(0, "end") for x in Entry_list]

        # reset label color
        for l in Label_list:
            l.configure({"fg": "white"})

        # new random seed
        self.randint = random.randrange(0, 1000)

    def _calculate_points(self, iter_label: Label, score_label_1: Label, score_label_2: Label) -> None:
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

    def _end_game(self, root: Tk) -> None:
        # clear canvas
            for element in root.winfo_children():
                element.destroy()

            # Print the result
            end_label = Label(root, text=f'Ergebnis: {self.points_1}:{self.points_2}', font=("Times 40"), bg="#333333", width=20, height=1)
            end_label.pack(anchor="center")

    def _build_word(self, Entry_list: list) -> None:
        # iterate through every entry object in row
            for l in range(0, 5):
                # if entry is not empty
                if Entry_list[self.guess_numb * 5 + l].get() != "":
                    # append char
                    self.row_chars.append(Entry_list[self.guess_numb * 5 + l].get())
            # save word
            self.word = "".join(self.row_chars)
    
    def _check_word(self) -> list:
        occurrence_list = [None] * 5

        # find goal word
        self.goal_word = self.wordle_duden[self.randint]

        for i in range(0, 5):
            # get all occurances of the char
            char_goal_occ = [occ.start() for occ in re.finditer(self.word[i], self.goal_word)]
            # correct_chars = [occurrence_list[l] for l in char_goal_occ].count(2)

            # char_word_occ = [[occ.start() for occ in re.finditer(self.word[i], self.word)]]

            # correct position and char
            if self.word[i] == self.goal_word[i]:
                occurrence_list[i] = 2

            # correct char and the char is not green yet
            elif self.word[i] in self.goal_word and self.word[:i+1].count(self.word[i]) <= len(char_goal_occ):
                occurrence_list[i] = 1
            else:
                occurrence_list[i] = 0

        return occurrence_list
    
    def _color_entrys(self, Entry_list, Label_list):
        # color entrys and letters
        for k in range(0, len(self.word)):
            Entry_list[self.guess_numb * 5 + k].configure(state = "disabled")
            Entry_list[self.guess_numb * 5 + k].configure({"disabledbackground": self.color_dict[self.hits[k]]})
            # letter color
            for l in Label_list:
                if l["text"] == Entry_list[self.guess_numb * 5 + k].get():
                    l.configure({"fg":self.color_dict[self.hits[k]]})

    def _show_evaluation(self, root):
        # if the correct word is guessed
        if self.hits == [2, 2, 2, 2, 2]:
            # print message
            self.mess_label = Label(root, text="Korrekt!", font=("Times 40"), bg="#333333", width=12, height=1)
            self.mess_label.grid(row=7, column=4)

        # if the word is wrong and its the last try
        elif self.guess_numb == 5:
            # print the word
            self.mess_label = Label(root, text=f'Leider falsch! Das Wort ist: {self.goal_word}', font=("Times 40"), bg="#333333", width=30, height=1)
            self.mess_label.grid(row=7, column=4)

        # if the word is wrong
        else:
            # print fail message
            self.mess_label = Label(root, text=" Leider falsch!", font=("Times 40"), bg="#333333", width=12, height=1)
            self.mess_label.grid(row=7, column=4)
        
        # add to guess_numb
        self.guess_numb += 1

    def _change_player_color(self, player_label_1: Label, player_label_2: Label):
        if self.player == 1:
            player_label_1.configure(fg = "#2ca115")
            player_label_2.configure(fg = "#fff")
        else:
            player_label_2.configure(fg = "#2ca115")
            player_label_1.configure(fg = "#fff")


    


    