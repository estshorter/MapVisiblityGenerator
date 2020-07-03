import matplotlib.pyplot as plt
import numpy as np
import toml
from matplotlib.colors import LinearSegmentedColormap

list_cid = [
    "#3E60C1",
    "#597BF0",
    "#74A963",
    "#3E7E62",
    "#3E7E62",
    "#A5BD7E",
    "#A5BD7E",
    "#BFD2AF",
    "#BFD2AF",
    "#D0D2D2",
]

configs = toml.load("config.toml")
height = configs["height"]
width = configs["width"]
elev = np.load("map.npy")
cm = LinearSegmentedColormap.from_list("custom_cmap", list_cid, N=len(list_cid))

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
X, Y = np.mgrid[0:width, 0:height]
surf = ax.plot_surface(X, Y, elev, cmap=cm)
plt.show()
