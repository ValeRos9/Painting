import numpy as np
from tifffile import imread
import matplotlib.pyplot as plt
from pathlib import Path

def view_one_scan(nb,PATH,FOLDER):
    plt.figure()

    for i in range(1200,1201):
        filename = f"{PATH}{FOLDER}scan_{n:06d}.tif"
        data = imread(filename)
        data = data[1000:1200, 0:1300]
        img = np.array(data)

        plt.clf()
        vmin, vmax = np.percentile(img, (1, 99))
        plt.imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
        plt.title(filename)
        plt.pause(0.1)

    plt.show()


Volume = []
FOLDER = Path("/home/valentin97/Painting/recon")

files = sorted(FOLDER.glob("scan_*.tif"))[200:1251:4]

Volume = np.stack([
    imread(scan)[1000:1200, 0:1300]
    for scan in files
])

print(Volume.shape)
