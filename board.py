import tkinter

root = tkinter.Tk()
root.title("Soundboard")

def callback(idx):
    print("You pressed button", idx)

for i in range(20):
    buttons[i] = tkinter.Button(root, text=i, width=25,
        command=lambda j=i: callback(j))
    buttons[i].pack()

button = tkinter.Button(root, text='Stop', width=25, command=root.destroy)
button.pack()

root.mainloop()
