#Libraries
from __future__ import division
import numpy as np
import astra
from os import mkdir
from os.path import join, isdir
from imageio import get_writer, imwrite


class Tomography:

    def __init__(self,painting,proj_geom,algorithm):
        self.painting = painting
        self.proj_geom = proj_geom
        self.algorithm = algorithm

    def project(self):
        tomo_volume = np.moveaxis(self.painting.volume,0,-1)
        vol_geom = astra.create_vol_geom(tomo_volume.shape[1],tomo_volume.shape[2],tomo_volume.shape[0])
        projection_id, projections = astra.create_sino3d_gpu(tomo_volume,self.proj_geom,vol_geom)
        projections /= np.max(projections)
        astra.data3d.delete(projection_id)
        return projections

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
