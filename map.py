import matplotlib.pyplot as plt
import numpy as np
import toml
from matplotlib.colors import LinearSegmentedColormap
from opensimplex import OpenSimplex

# https://www.redblobgames.com/maps/terrain-from-noise/
# https://qiita.com/HidKamiya/items/524d77e3b53a13849f1a
gen = OpenSimplex()


def noise(nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    return gen.noise2d(nx, ny) / 2.0 + 0.5


configs = toml.load("config.toml")
height = configs["height"]
width = configs["width"]
c = configs["coef"]

elev = np.empty((height, width))
for y in range(height):
    for x in range(width):
        nx = x / width - 0.5
        ny = y / height - 0.5
        e = (
            noise(c * nx, c * ny)
            + 0.5 * noise(c * 2 * nx, c * 2 * ny)
            + 0.25 * noise(c * 4 * nx, c * 4 * ny)
        )
        elev[y, x] = e
elev = elev ** 1.6
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
