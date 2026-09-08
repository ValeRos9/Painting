#Libraries
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
#import pyvista as pv

import astra
import flexdata
from os import mkdir
from os.path import join, isdir
from imageio import get_writer, imwrite


class Painting_generator:
    def __init__(self,dim_x,dim_y,thickness,intensity,N_spheres,radius):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.thickness = thickness
        self.intensity = intensity
        self.N_spheres = N_spheres 
        self.radius = radius


    def paint(self):
        layers = []
        for i in range(self.thickness.size):
            layer = self.generate_cst_volume(self.thickness[i], self.dim_x, self.dim_y, self.intensity[i])
            if i == 0:
                self.random_insert_sphere(layer, self.N_spheres, self.radius, 100)  # modifies first layer only
            layers.append(layer)  # add to list  
        return Painting(np.concatenate(layers, axis=0))

    @staticmethod
    def generate_cst_volume(length,rows,cols,intensity):
        "creates 3d volume with same value"
        cst_volume = np.full((length, cols, rows), intensity,dtype=float)
        return cst_volume

    @staticmethod
    def insert_sphere(layer,xc,yc,zc,r,intensity):
        """Insert a sphere into layer"""
        Z, X, Y = layer.shape
        x_coords, y_coords, z_coords = np.meshgrid(np.arange(X), np.arange(Y), np.arange(Z), indexing='ij')
        dist_sq = (x_coords - xc)**2 + (y_coords - yc)**2 + (z_coords - zc)**2
        layer[np.any(dist_sq <= r**2, axis=0)] = intensity

    @staticmethod
    def random_insert_sphere(layer, N_spheres, r, intensity):
        """Insert spheres at random into a layer """
        x, y, z = np.meshgrid(np.arange(layer.shape[0]), np.arange(layer.shape[1]), np.arange(layer.shape[2]), indexing='ij')
        centers = Painting_generator.select_random_indices(layer,N_spheres)
        xc = centers[:, 1, np.newaxis, np.newaxis, np.newaxis] 
        yc = centers[:, 2, np.newaxis, np.newaxis, np.newaxis] 
        zc = centers[:, 0, np.newaxis, np.newaxis, np.newaxis] 
        dist_sq = (x - xc)**2 + (y - yc)**2 + (z - zc)**2
        layer[np.any(dist_sq <= r**2, axis=0)] = intensity
        ##I would check that this actually does what you would like to have done
        ##Check that spheres are within boundaries and that they don't overlap

    @staticmethod
    def select_random_indices(layer,N):
        """Picks random indices from a flattened list and returns indices array (Nx3)"""
        indices_flat = np.random.choice(layer.size, size=N, replace=False)
        return np.array(np.unravel_index(indices_flat, layer.shape)).T


class Painting:
    def __init__(self,volume):
        self.volume = volume

""" Options: 1. Painting class which means it's the same instance of the clas, 2. Geometry and it's a new np or the way it is currently
    def modify_orientation(self):
        self.volume = np.moveaxis(self.volume,0,-1)
"""

class Geometry:

    def __init__(self,Painting,SO,OD,n_proj,geometry_type,det_x,det_y,spacing_x,spacing_y):
        self.Painting = Painting
        self.SO = SO
        self.OD = OD
        self.n_proj = n_proj
        self.geometry_type = geometry_type
        self.det_x = det_x
        self.det_y = det_y
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y

    def projection(self):
        shift = np.pi/2
        angles = np.linspace(0+shift,2*np.pi+shift, num=self.n_proj, endpoint=False)
        proj_geom = astra.create_proj_geom(self.geometry_type, self.spacing_x, self.spacing_y, self.det_x, self.det_y,angles,self.SO,self.OD)
        return proj_geom
                               
    
class Tomography:

    #Problems:
    #Projections_id is it self, how do you delete it ? I'm starting to doubt if you can give the class attributes as you go along
    def __init__(self,painting,algorithm,proj_geom):
        self.painting = painting
        self.algorithm = algorithm
        self.proj_geom = proj_geom

    def project(self):
        tomo_volume = np.moveaxis(self.painting.volume,0,-1)
        vol_geom = astra.create_vol_geom(tomo_volume.shape[1],tomo_volume.shape[2],tomo_volume.shape[0])
        projection_id, projections = astra.create_sino3d_gpu(tomo_volume,self.proj_geom,vol_geom)
        projections /= np.max(projections)
        astra.data3d.delete(projection_id)
        return projections

        #you can run a test by give it projections and remaking the id

    def reconstruct(self,projections):
        vol_geom = astra.creators.create_vol_geom(projections.shape[0], projections.shape[0],projections.shape[2])
        projection_id = astra.data3d.create('-sino', self.proj_geom, projections)
        reconstruction_id = astra.data3d.create('-vol', vol_geom, data=0)
        alg_cfg = astra.astra_dict(self.algorithm)
        alg_cfg['ProjectionDataId'] = projection_id
        alg_cfg['ReconstructionDataId'] = reconstruction_id
        algorithm_id = astra.algorithm.create(alg_cfg)
        astra.algorithm.run(algorithm_id)
        reconstructions = astra.data3d.get(reconstruction_id)
        reconstructions[reconstructions < 0] = 0
        reconstructions /= np.max(reconstructions)
        reconstructions = np.round(reconstructions * 255).astype(np.uint8)
        astra.algorithm.delete(algorithm_id)
        astra.data3d.delete(reconstruction_id)
        astra.data3d.delete(projection_id)
        return reconstructions 

    @staticmethod
    def add_noise(projections):
        projections = np.random.poisson(projections * 10000) / 10000
        projections[projections > 1.1] = 1.1
        projections /= 1.1
        return noisy_projections

    @staticmethod
    def save_projections(folder,projections):
        if not isdir(folder):
            mkdir(folder)
        projections = np.round(projections * 65535).astype(np.uint16)
        for i in range(projections.shape[1]):
            projection = projections[:, i, :]
            with get_writer(join(folder, 'proj%04d.tif' %i)) as writer:
                writer.append_data(projection, {'compress': 9})
    
    @staticmethod
    def save_reconstruction(folder,reconstruction):
        if not isdir(folder):
            mkdir(folder)
        for i in range(reconstruction.shape[0]):
            im = reconstruction[i, :, :]
            im = np.flipud(im)
            imwrite(join(folder, 'reco%04d.png' % i), im)

"""
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
"""

#Generate Painting 
artist = Painting_generator(dim_x=100,dim_y=100,thickness=np.array([10]),intensity=np.array([10]),N_spheres=3,radius=10)
painting = artist.paint()

#Generate geometries 
Geom = Geometry(painting,SO=1000,OD=200,n_proj=180,geometry_type='cone',det_x=512,det_y=512,spacing_x=1,spacing_y=1)
proj_geom = Geom.projection()

#projection and reconstruction 
Tomo = Tomography(painting,'FDK_CUDA',proj_geom)
projections = Tomo.project()
slices = Tomo.reconstruct(projections) 
Tomo.save_projections('projections',projections)
Tomo.save_reconstruction('slices',slices)


#Work Flow:
#1. The reconstruction didn't work because of the geometry you gave the system 
#2. Read about sphere insertions, FOAM (Frederik said a non-random insertion might also be good enough)
#3. Watch class video
#4. Plan next steps: finish up sphere insertion and x-ray lib 


#Remarks:
#1.Thickness and Intensity are currently numpy arrays, the way you coded them requires this format, does this make the most sense ?
#Perhaps a user once the option to modify specific layers or enter an int for the thickness or intensity 
#Learn about: 1. debugging and 2. unit testing 
#Placing spheres at random, how large can it get ? consider points and radius 
#Foam paper, does MC use it ?
#3.Generate frame and nails 
