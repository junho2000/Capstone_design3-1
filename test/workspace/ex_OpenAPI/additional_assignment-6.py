import RPi.GPIO as GPIO
import tkinter as tk

LED1 = 4 #red
LED2 = 2 #green
LED3 = 3 #yellow

red = 0
green = 0
yellow = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED3, GPIO.OUT, initial=GPIO.LOW)

def LED_On():
    global red
    global green
    global yellow
    LED_Off()
    if red == 1:
        GPIO.output(LED1, 1)
    if green == 1:
        GPIO.output(LED2, 1)
    if yellow == 1:
        GPIO.output(LED3, 1)
def LED_Off():
    GPIO.output(LED1, 0)
    GPIO.output(LED2, 0)
    GPIO.output(LED3, 0)

def Led_color():
    global red
    global green
    global yellow
    
    if color.get() == 0:
        red = 1
        green = 0
        yellow = 0
    elif color.get() == 1:
        red = 0
        green = 1
        yellow = 0
    elif color.get() == 2:
        red = 0
        green = 0
        yellow = 1
 
 
root = tk.Tk()

root.title("Button Examples")
root.geometry("300x400")
root.option_add('*Font', '20') #font size

color = tk.IntVar()
rad1 = tk.Radiobutton(root, text='Red', variable=color, value=0, command=Led_color)

rad2 = tk.Radiobutton(root, text='Green', variable=color, value=1, command=Led_color)

rad3 = tk.Radiobutton(root, text='Yellow', variable=color, value=2, command=Led_color)


label = tk.Label(root, text='LED On and Off Program')
label.pack(padx=10, pady=10)

btn1 = tk.Button(root, width=10, height=2, fg="yellow", bg="red", text="LED ON", command=LED_On)
btn1.pack(padx=5,pady=5)

btn2 = tk.Button(root, width=10, height=2, fg="yellow", bg="green", text="LED OFF", command=LED_Off)
btn2.pack(padx=5,pady=5)

rad1.pack()
rad2.pack()
rad3.pack()


root.mainloop()
GPIO.cleanup()



