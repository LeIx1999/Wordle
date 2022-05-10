# Game GUI
from tkinter import *

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

# Entrys for letters
row = 0
column_list = [0, 1, 2, 3, 4] * 6
for i in range(0, 30):
    if i <= 2:
        Entry(main_frame,width = 4, font=("", 40), validate="key", validatecommand=letter_cmd).grid(row = row, column = column_list[i])
    else:
        Entry(main_frame, width = 4, font=("", 40), validate="key", validatecommand=letter_cmd).grid(row=int(i/5), column=column_list[i])


# alphabet labels
letters_list = ["q", "w", "e", "r", "t", "z", "u", "i", "o", "p", "ü", "a", "s", "d",
                "f", "g", "h", "j", "k", "l", "ö", "ä", "y", "x", "c", "v", "b", "n", "m"]
column_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 2
column_list = column_list + [2 ,3, 4, 5, 6, 7, 8]

for i in range(0, 29):
    Label(second_frame, text=letters_list[i], font=("Times 40"), bg="darkgrey", width = 1, height=1).grid(row=int(i/11), column= column_list[i])

# Mainloop
root.mainloop()