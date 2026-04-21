#libraries 
from __future__ import division
import numpy as np
import astra
#import tomosipo as ts 

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
    
    """
    def tomosipo_visualization(self):
        vg = ts.volume(
            shape=(self.Painting.volume.shape[1],self.Painting.volume.shape[2],self.Painting.volume.shape[3]),
            size=(self.Painting.volume.shape[1],self.Painting.volume.shape[2],self.Painting.volume.shape[3]),
            pos=(0,0,0),
        )
        pg = ts.cone(
            angles=180,
            shape=self.Painting.volume.shape[2],
            src_OD=self.SO,
            src_DD=self.OD
            )



        vg = ts.volume_vec(
            shape=(self.Painting.volume.shape[1],self.Painting.volume.shape[2],self.Painting.volume.shape[3]),
            pos=[(0,0,0)],
            w=[(1,0,0)],
            v=[(0,1,0)],
            u=[(0,0,1)],
            )
        pg = ts.cone_vec(
            shape= (self.det_x,self.det_y),
            src_pos= [(0,self.SO,0)]
            det_pos=[(0,self.OD,0)]
            det_v= [(self.spacing_x,0,0)] #maybe the spacing are off
            det_u= [(0,0,self.spacing_y)]
        )
        
        visual  = ts.svg(vg,pg)
        return visual
        """