import tkinter as tk

root = tk.Tk()

root.title("Kookmin University") #title
root.option_add('*Font', '20') #font size
root.geometry("300x200") #window size

label = tk.Label(root, text='Hello Kookmin!')
label.pack(padx=10, pady=10)

root.mainloop()