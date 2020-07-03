import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from opensimplex import OpenSimplex

# https://www.redblobgames.com/maps/terrain-from-noise/
# https://qiita.com/HidKamiya/items/524d77e3b53a13849f1a
gen = OpenSimplex()


def noise(nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    return gen.noise2d(nx, ny) / 2.0 + 0.5


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

height = 200
width = 200
c = 8

elev = np.empty((height, width))
for y in range(height):
    for x in range(width):
        nx = x / width - 0.5
        ny = y / height - 0.5
        e = (
            1 * c * noise(1 * c * nx, 1 * c * ny)
            + 0.5 * noise(c * 2 * nx, c * 2 * ny)
            + 0.25 * noise(c * 4 * nx, c * 4 * ny)
            + 0.125 * noise(c * 8 * nx, c * 8 * ny)
        )
        elev[y, x] = e
elev = elev ** 1.2
maxv = elev.flatten().max()
elev /= maxv
cm = LinearSegmentedColormap.from_list("custom_cmap", list_cid, N=len(list_cid))

plt.imshow(elev, cmap=cm, interpolation="nearest", vmin=0, vmax=1)
plt.colorbar()
# plt.show()
plt.savefig("map.png", dpi=300, bbox_inches="tight")
np.save("map.npy", elev)
