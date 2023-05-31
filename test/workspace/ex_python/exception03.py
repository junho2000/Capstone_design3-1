a = ['a', 'b', 'c']

number = int(input('Input a number > '))

try:
    b = a[number]

except IndexError:
    print('Index Error!')

else:
    print(b)

finally:
    print('end of program')