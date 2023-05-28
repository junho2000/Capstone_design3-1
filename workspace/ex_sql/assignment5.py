import tkinter as tk
import RPi.GPIO as GPIO

LED = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

def LED_onoff():
    GPIO.output(LED, not GPIO.input(LED))
    
root = tk.Tk()

label = tk.Label(root, text='Press button!')
label.pack(padx=10, pady=10)

button = tk.Button(root, text="button", command=LED_onoff)
button.pack(padx=20, pady=20)

root.mainloop()
GPIO.cleanup()