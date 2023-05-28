import RPi.GPIO as GPIO
import tkinter as tk

# segment radio
# led pwm slide

LED = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

def LED_On():
    GPIO.output(LED, 1)
def LED_Off():
    GPIO.output(LED, 0)
    
    
root = tk.Tk()

root.title("Button Examples")
root.geometry("300x200")
root.option_add('*Font', '20') #font size

label = tk.Label(root, text='LED On and Off Program')
label.pack(padx=10, pady=10)

btn1 = tk.Button(root, width=10, height=2, fg="yellow", bg="red", text="LED ON", command=LED_On)
btn1.pack(padx=5,pady=5)

btn2 = tk.Button(root, width=10, height=2, fg="yellow", bg="green", text="LED OFF", command=LED_Off)
btn2.pack(padx=5,pady=5)

root.mainloop()
GPIO.cleanup()


