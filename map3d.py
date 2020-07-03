import matplotlib.pyplot as plt
import numpy as np
import toml
from matplotlib.colors import LinearSegmentedColormap

configs = toml.load("config.toml")
height = configs["height"]
width = configs["width"]
elev = np.load("map.npy")
map_cm_colorcode = configs["map_cm_colorcode"]
cm = LinearSegmentedColormap.from_list(
    "custom_cmap", map_cm_colorcode, N=len(map_cm_colorcode)
)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
X, Y = np.mgrid[0:width, 0:height]
surf = ax.plot_surface(X, Y, elev, cmap=cm)
plt.show()
