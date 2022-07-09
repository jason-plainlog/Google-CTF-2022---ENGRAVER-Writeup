# Google-CTF-2022---ENGRAVER-Writeup
> Jason1024 @ Balsn

To find the robot arm model, packet #16 hints at the manufacturer: Hiwonder. After browsing the robot arms produced by Hiwonder, we discovered that the leArm matches the robot arm appearance shown in the pictures.

![](https://i.imgur.com/YlRMOAQ.png)
> The #16 packet reveals the manufacturer of the robot arm

After googling the datasets for such a model, we found [an official communicate protocol dataset.](https://drive.google.com/file/d/1Q4tfXqKED5C4j5z694H6Q5I2bnEpW_mQ/view?usp=sharing) With the dataset, identifying the servo commands from the packets becomes possible.

![](https://i.imgur.com/wK2bdrq.png)

We can dump the servo command packets with the filter: `(usb.src == "host") && (usbhid.data contains 55:55:08:03)` and extract the HID data using wireshark:

```
HID Data: 5555080301f40101fc080000000000000000000000000000000000000000000000000000…
HID Data: 5555080301dc050214050000000000000000000000000000000000000000000000000000…
HID Data: 5555080301dc0503a4060000000000000000000000000000000000000000000000000000…
HID Data: 5555080301dc0504c4090000000000000000000000000000000000000000000000000000…
HID Data: 5555080301dc050540060000000000000000000000000000000000000000000000000000…
HID Data: 5555080301dc0506dc050000000000000000000000000000000000000000000000000000…
...
```

Then by referencing the official document, we can understand the servo being controlled and the angle specified in each command. We can also identify a reset sequence (by moving servo 1 to servo 6 to the same position, as shown above) that happens before writing every letter. Only three servos are moved in the commands by excluding the reset sequence. We can guess that two of which are the x and y coordinate, and the other one is for controlling the light of the laser pen, and the value of such one should be flipping between two different values. Thus we found servo 1 (which only has two possible angles in the commands 23 and 24) to be the light controlling servo, and servos 2 & 3 are for positioning. Then, by simulating the servos and plotting the light trace in matplot, we got the flag: `CTF{6_DEGREES_OF_FR3EDOM}`


Final payload:

```python=
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
```
