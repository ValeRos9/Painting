import numpy as np
from tifffile import imread
import matplotlib.pyplot as plt
from pathlib import Path

def view_one_scan(nb,FOLDER):
    plt.figure()

    for i in range(1200,1201):
        filename = f"{FOLDER}scan_{n:06d}.tif"
        data = imread(filename)
        data = data[1000:1200, 0:1300]
        img = np.array(data)

        plt.clf()
        vmin, vmax = np.percentile(img, (1, 99))
        plt.imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
        plt.title(filename)
        plt.pause(0.1)

    plt.show()

def plot_3D_volume(volume):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Get middle indices for each dimension
    dz, dy, dx = volume.shape
    mid_z, mid_y, mid_x = dz // 2, dy // 2, dx // 2

    # 1. XY Plane (Top View)
    axes[0].imshow(volume[mid_z, :, :], cmap='gray')
    axes[0].set_title(f'XY Slice (Z={mid_z})')
    axes[0].axis('off')

    # 2. XZ Plane (Side View)
    axes[1].imshow(volume[:, mid_y, :], cmap='gray')
    axes[1].set_title(f'XZ Slice (Y={mid_y})')
    axes[1].axis('off')

    # 3. YZ Plane (Front View)
    axes[2].imshow(volume[:, :, mid_x], cmap='gray')
    axes[2].set_title(f'YZ Slice (X={mid_x})')
    axes[2].axis('off')

    plt.tight_layout()
    plt.show()

# Call the function
plot_3D_volume(Volume)



FOLDER = Path("/home/valentin97/Painting/recon")
files = sorted(FOLDER.glob("scan_*.tif"))[200:1251:20]

Volume = []
Volume = np.stack([
    imread(scan)[1000:1200, 0:1300]
    for scan in files
])

z, y, x = np.indices(Volume.shape)

fig = go.Figure(go.Volume(
    x=x.flatten(),
    y=y.flatten(),
    z=z.flatten(),
    value=Volume.flatten(),
    isomin=15000,
    isomax=50000,
    opacity=0.5,
    surface_count=15
))

fig.show()


print(Volume.shape)
