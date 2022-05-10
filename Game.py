
# Create word list
with open("Duden") as file:
    Document = file.readlines()

# Clean Document
Document = [x.replace("\n", "") for x in Document]
wordle_duden = []