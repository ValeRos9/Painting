#libraries 
from __future__ import division
import numpy as np
import astra
import tomosipo as ts 
import torch

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
    

