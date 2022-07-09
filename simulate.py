import numpy as np
import matplotlib.pyplot as plt

opes = []
with open('trace.txt', 'r') as f:
    for line in f.readlines():
        line = line.split()[2][10:20]
        time = int(line[2:4] + line[:2], 16) // 100
        survo = int(line[4:6])
        angle = int(line[8:] + line[6:8], 16) // 100
        opes.append((survo, angle))

i, light = 0, False
x, y = 0, 0
path = []
while i < len(opes) - 6:
    # reset
    if opes[i:i+6] == [(1, 23), (2, 13), (3, 17), (4, 25), (5, 16), (6, 15)]: 
        x, y, light = 13, 17, False

        plt.xlim([-16, -12])
        plt.ylim([14, 18])
        plt.plot(*np.array(path).T)
        plt.show()
        path = []

        i += 6
        continue

    ope = opes[i]
    if ope[0] == 1:
        if ope[1] == 24:
            print("light on!")
            light = True
        elif ope[1] == 23:
            print("light off!")
            light = False
    elif ope[0] == 2:
        if ope[1] < x:
            print("move right!")
        elif ope[1] > x:
            print("move left!")
        x = ope[1]
    elif ope[0] == 3:
        if ope[1] < y:
            print("move down!")
        elif ope[1] > y:
            print("move up!")
        y = ope[1]
    i += 1

    print((x, y))
    if light:
        path.append((-x, y))
