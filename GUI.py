from tkinter import *
from tkinter import messagebox
window = Tk()
window.title("Veo cơm tu GUI")
window.geometry("800x400")
window.configure(bg='#02162D')

# Test def
def helloCallBack():
    messagebox.showinfo("Information","Information for user")


def welcomeMessage():
    name = entryBox.get()
    return messagebox.showinfo('message', f'Hi! {name}, Welcome to python guides.')


# the label for user_name
label = Label(window, text="Label 1")
label.grid(row=1, column=2, sticky=W)
# user_name_input_area = Entry(window, width = 30).place(x = 110, y = 60)
entryBox = Entry(window,width=60)
entryBox.grid(row=2, column=2,sticky=W)
submit_button = Button(window,text="Click Here" , command = welcomeMessage).place(x=40, y=130)

window.mainloop()

#