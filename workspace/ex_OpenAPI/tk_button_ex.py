import tkinter as tk

root = tk.Tk()
root.title("Button Examples")
root.geometry("300x400")

btn1 = tk.Button(root, text="Button 1")
btn1.pack(padx=5,pady=5) #yeoback setting

btn2 = tk.Button(root, width=20, height=3, text="Button 2")
btn2.pack(padx=5,pady=5)

btn3 = tk.Button(root, width=10, height=2, fg="yellow", bg="green", text="Button 3")
btn3.pack(padx=5,pady=5)

def btncmd():
    print("Hello, Kookmin University!")

photo = tk.PhotoImage(file="benz.png")
btn4 = tk.Button(root, image=photo, command=btncmd)
btn4.pack(padx=5,pady=5)

root.mainloop()

