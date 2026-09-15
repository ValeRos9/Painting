import numpy as np
from tifffile import imread
from pathlib import Path

FOLDER = Path("/home/valentin97/Downloads/Painting/recon")
files = sorted(FOLDER.glob("scan_*.tif"))[200:1251:20]

V = np.stack([
    imread(f)[1080:1200,0:1300] for f in files 
    ])

np.save("Volume.npy",Volume)
print("Volume saved remotely!")



# import numpy as np
# from tifffile import imread
# from pathlib import Path
# import pyvista as pv
# import napari

# def view_one_scan(nb,FOLDER):
#     plt.figure()

#     for i in range(1200,1201):
#         filename = f"{FOLDER}scan_{n:06d}.tif"
#         data = imread(filename)
#         data = data[1000:1200, 0:1300]
#         img = np.array(data)

#         plt.clf()
#         vmin, vmax = np.percentile(img, (1, 99))
#         plt.imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
#         plt.title(filename)
#         plt.pause(0.1)

#     plt.show()

# FOLDER = Path("/home/valentin97/Downloads/Painting/recon")
# files = sorted(FOLDER.glob("scan_*.tif"))[200:1251:4]

# Volume = []
# Volume = np.stack([
#     imread(scan)[1080:1200, 0:1300]
#     for scan in files
# ])

# print(Volume.shape)

# #pv.wrap(Volume).plot(volume=True)
# # plotter = pv.Plotter()
# # plotter.add_volume(Volume)
# # plotter.add_mesh_clip_plane(pv.wrap(Volume))
# # plotter.show()

# viewer = napari.Viewer()
# viewer.add_image(Volume)
# napari.run()