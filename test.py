import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()
dimension = (3, 3)
data = np.random.rand(dimension[0], dimension[1])
sns.heatmap(data, vmax=.8)

def init():
    sns.heatmap(np.zeros(dimension), vmax=.8, cbar=False)

def animate(i):
    data = np.random.rand(dimension[0], dimension[1])
    sns.heatmap(data, vmax=.8, cbar=False)

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=20, repeat=False)

plt.show()