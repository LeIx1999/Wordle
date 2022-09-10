import json
import random
# Create word list
with open("Duden_deutsch.txt", encoding = "utf8") as file:
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

# %%
