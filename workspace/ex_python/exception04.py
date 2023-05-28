import time

try:
    while True:
        print("program is running. (Press ctrl+c to stop)")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program is stopped!")
    
finally:
    print('End of program')