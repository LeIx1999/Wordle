import json
import random
# Create word list
with open("Duden") as file:
    Document = file.readlines()

# Clean Document
wordle_duden = [x.replace("\n", "") for x in Document]
wordle_duden = [x.lower() for x in wordle_duden]

# replace Umlaute
character = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
for i in range(0, len(wordle_duden)):
    for char in character:
        wordle_duden[i] = wordle_duden[i].replace(char, character[char])

# take only 5 char words
wordle_duden = [wordle_duden.remove(word) if len(word) != 5 else word for word in wordle_duden]

# remove None
wordle_duden = list(filter(None, wordle_duden))

# save wordle_duden
with open("wordle_duden.json", "w") as duden:
    json.dump(wordle_duden, duden, indent=2)

# Function to check the accuracy of the input word
def check_word(word, randint, duden):
    occurrence_list = []


    # find goal word
    goal_word = duden[randint]

    for i in range(0, 5):
        # correct position and char
        if word[i] == goal_word[i]:
            occurrence_list.append(2)
        # correct char
        elif word[i] in goal_word:
            occurrence_list.append(1)
        else:
            occurrence_list.append(0)

    return occurrence_list, goal_word

check_word("franz", 3, wordle_duden)



