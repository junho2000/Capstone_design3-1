import tkinter as tk

root = tk.Tk()

root.title("Button Test")

label = tk.Label(root, text = 'Hello Kookmin!')
label.pack()

def button_clicked():
    print("button clicked")
    
button = tk.Button(root, text="Click me", width=10, command=button_clicked)
button.pack(padx=10, pady=10)

root.mainloop()