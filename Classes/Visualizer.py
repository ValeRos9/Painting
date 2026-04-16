import numpy as np
#import pyvista as pv 



class Visualizer: 
    def __init__(self,painting):
        self.painting = painting
        self.oil_intensity = 50
        self.particle_intensity = 100

    def generate_3d_visual(self):       
        coords_50 = np.argwhere(self.painting.volume == self.oil_intensity)
        coords_100 = np.argwhere(self.painting.volume == self.particle_intensity)
        cloud_50 = pv.PolyData(coords_50)
        cloud_100 = pv.PolyData(coords_100)
        plotter = pv.Plotter()
        plotter.add_mesh(cloud_50, color='red', point_size=10, render_points_as_spheres=True, opacity=0.1)
        plotter.add_mesh(cloud_100, color='blue', point_size=10, render_points_as_spheres=True, opacity=1.0)
        plotter.show()