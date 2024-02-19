import random
from matrices import solve
from matplotlib import pyplot as plt
import numpy as np

x = np.linspace(0, 1000, 500)
y = np.array([10 * (0.5 + random.random()/2) * n + 16 + random.randint(0, 50) * random.random() for n in x])

m = np.array([[sum(xi ** 2 for xi in x), sum(x)], [sum(x), len(x)]])
r = np.array([[sum(xi * yi for xi, yi in zip(x, y))], [sum(y)]])

a, b = solve(m, r)


plt.scatter(x, y)

g = np.linspace(1, 1000, 1000)
h = list(a*j + b for j in g)

plt.plot(g, h)
plt.plot(g,[10 * x + 16 for x in g])

plt.show()
