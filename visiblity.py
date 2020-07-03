import matplotlib.pyplot as plt
import numpy as np
from bresenham import bresenham
from matplotlib.colors import LinearSegmentedColormap

list_cid1 = [
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
list_cid2 = [
    "#FFFFFF",
    "#FFCDCD",
    "#FF0000",
]
cm1 = LinearSegmentedColormap.from_list("custom_cmap", list_cid1, N=len(list_cid1))
cm2 = LinearSegmentedColormap.from_list("custom_cmap", list_cid2, N=len(list_cid2))

e = np.load("map.npy")

e[e < 0.1] = 0
e[np.logical_and(0.1 <= e, e < 0.2)] = 0.1
e[np.logical_and(0.2 <= e, e < 0.3)] = 0.2
e[np.logical_and(0.3 <= e, e < 0.5)] = 0.4
e[np.logical_and(0.5 <= e, e < 0.7)] = 0.6
e[np.logical_and(0.7 <= e, e < 0.9)] = 0.8
e[0.9 <= e] = 1


def visiblity(b, vis, elev_obs):
    next(b)
    for line_pos in b:
        if e[line_pos] > elev_obs:
            break
        vis[line_pos] = 0.5


def generate_visiblity_map(*pos_obs):

    vis = np.zeros((height, width))
    elev_obs = e[pos_obs]
    vis[pos_obs] = 1

    for w in range(width):
        visiblity(bresenham(*pos_obs, w, 0), vis, elev_obs)
        visiblity(bresenham(*pos_obs, w, height - 1), vis, elev_obs)
    for h in range(height):
        visiblity(bresenham(*pos_obs, width - 1, h), vis, elev_obs)
        visiblity(bresenham(*pos_obs, 0, h), vis, elev_obs)

    plt.imshow(e, cmap=cm1, interpolation="nearest", vmin=0, vmax=1)
    plt.colorbar()
    cm2.set_under(alpha=0)
    plt.imshow(vis, cmap=cm2, interpolation="nearest", vmin=0.001, vmax=1, alpha=0.6)

    # plt.show()
    plt.savefig(f"visiblity_{pos_obs}.png", dpi=300, bbox_inches="tight")
    plt.close()
    vis[vis > 0.1] = 1
    return vis


height = 200
width = 200

generate_visiblity_map(0, 0)
generate_visiblity_map(100, 100)
generate_visiblity_map(110, 110)
