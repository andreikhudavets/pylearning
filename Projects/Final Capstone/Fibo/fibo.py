#!/usr/bin/env python

"""
Enter a number and have the program generate the Fibonacci sequence to that number or to the Nth number.
"""
def fibo():
    (x1, x2) = (0, 1)
    while True:
        yield x1
        (x1, x2) = (x2, x1+x2)

while True:
    (max_value, max_index) = (0, 0)
    user_string = raw_input("Please enter limits: count=<N> or value=<N>")
    try:
        (command, number) = user_string.split('=')
        if command == "count":
            max_index = int(number)
        elif command == "value":
            max_value = int(number)
        elif command == "e":
            break
        else:
            continue
    except:
        continue
    else:
        for (i, f) in enumerate(fibo()):
            if ((i > max_index and max_index > 0) or (f > max_value and max_value >0) or (max_index <=0 and max_value <=0)):
                break
            print f