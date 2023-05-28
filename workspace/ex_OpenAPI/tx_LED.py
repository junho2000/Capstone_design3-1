import RPi.GPIO as GPIO
import tkinter as tk

LED = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

def LED_Onoff():
    GPIO.output(LED, not GPIO.input(LED))
    
root = tk.Tk()

label = tk.Label(root, text='Press Button')
label.pack(padx=10, pady=10)

button = tk.Button(root, text='Button', command=LED_Onoff)
button.pack(padx=20,pady=20)

root.mainloop()
GPIO.cleanup()