import matplotlib.pyplot as plt
import numpy as np
import toml
from matplotlib.colors import LinearSegmentedColormap
from opensimplex import OpenSimplex

# https://www.redblobgames.com/maps/terrain-from-noise/
# https://qiita.com/HidKamiya/items/524d77e3b53a13849f1a

configs = toml.load("config.toml")
height = configs["height"]
width = configs["width"]
c = configs["coef"]

gen = OpenSimplex(configs["seed"])


def noise(nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    return gen.noise2d(nx, ny) / 2.0 + 0.5


elev = np.empty((height, width))
for y in range(height):
    for x in range(width):
        nx = (x / width - 0.5) * c
        ny = (y / height - 0.5) * c
        e = noise(nx, ny) + 0.5 * noise(2 * nx, 2 * ny) + 0.25 * noise(4 * nx, 4 * ny)
        elev[y, x] = e
elev **= 1.6
emin = elev.flatten().min()
elev -= emin
emax = elev.flatten().max()
elev /= emax

map_cm_colorcode = configs["map_cm_colorcode"]
cm = LinearSegmentedColormap.from_list(
    "custom_cmap", map_cm_colorcode, N=len(map_cm_colorcode)
)

plt.imshow(elev, cmap=cm, interpolation="nearest", vmin=0, vmax=1)
plt.colorbar()
# plt.show()
plt.savefig("map.png", dpi=300, bbox_inches="tight")
np.save("map.npy", elev)
