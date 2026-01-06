import matplotlib.pyplot as plt
import numpy as np

steps = 100

exp = 2

max = pow(steps, exp)


arr = []
for i in range(steps):
    i += 1
    num = 0


    x = i / steps

    if (x < .5):
        num =  4 * x * x * x 
    else:
        num = 1 - pow(-2 * x + 2, 3) / 2


    arr.append(1-num)

    



xpoints = np.array([i for i in range(steps)])
ypoints = np.array(arr)
plt.plot(xpoints, ypoints)

plt.show()