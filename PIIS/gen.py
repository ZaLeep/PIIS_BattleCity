import random as rd
import numpy as np

for j in range(1, 11):
    result = ""
    for i in range(rd.randint(150, 300)):
        if rd.randint(1, 100) < 70:
            result += chr(rd.randint(97, 122))
        else:
            result += str(rd.randint(0,9))
        if rd.randint(1, 100) < 20:
            result += '.'
        if i != 0 and i % 20 == 0:
            result += '\n'
    print(result)
    f = open("D:\Course III\WEB_Java\Lab_1\Test2\\test2_" + str(j) + ".txt", "w")
    f.write(result)