import tomosipo as ts 
import torch 
import numpy as np
from os import mkdir
from os.path import join, isdir
from timeit import default_timer as timer
from scipy.ndimage import zoom
import tifffile


#Explantion of Geometries: https://aahendriksen.gitlab.io/tomosipo/topics/geometries.html#topics-geometries
#Example of object being rotated: https://aahendriksen.gitlab.io/tomosipo/intro/lab_frame.html
#TO-DO
#. We've got tomosipo on the remote, changed remote conda env from Painting to tomo_env
#. We need to check if projections and reconstruction are visually sound 
#. Figure out SVG and the jupyter notebook
#. Figure out how to implement varying geometries 
#. Update the layout 

class Tomo:

    def __init__(self,volume,n_proj,det_row,det_col,SO,OD,spacing_x,spacing_y,Nx,Ny,Nslices):
        self.volume = np.moveaxis(volume,0,-1)
        self.n_proj = n_proj
        self.det_row = det_row
        self.det_col = det_col
        self.SO = SO
        self.OD = OD
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.Nx = Nx
        self.Ny = Ny
        self.Nslices = Nslices
        print(self.volume.shape)

    def operator(self):
        #set projection geometry (handles resolution,sampling, etc of projection images)
        pg = ts.cone_vec(shape=(self.det_row,self.det_col), src_pos=(0,-self.SO,0), det_pos=(0,self.OD,0), 
            det_v=(self.spacing_x, 0, 0), det_u=(0, 0, self.spacing_y))
        #example: if det_row= 512 (amount of pixels) and det_v=0.5 (pixel_step) -> 512x0.5=256 (physical size)
        print(pg)

        #set volume geometry (handles resolution,sampling, etc of reconstruction images)
        dw = self.volume.shape[0]/self.Nx
        dv = self.volume.shape[1]/self.Ny
        du = self.volume.shape[2]/self.Nslices

        vg = ts.volume_vec(shape=(self.Nx,self.Ny,self.Nslices),pos=(0,0,0), 
            w=(dw,0,0), v=(0,dv,0), u=(0,0,du))
        print(vg)
        #example: if Nx = 256 (pixels) and dw = 100/256 (pixel_step) -> 256x100/256=100 (physical size)

        #Create rotation geometry and apply
        angles = np.linspace(np.pi/2, 2*np.pi+np.pi/2, self.n_proj, endpoint=False)
        axis_pos = (0,0,0)
        axis_direction = (1,0,0)
        R = ts.rotate(pos=axis_pos, axis=axis_direction, angles=angles)
        vg_rot = R * vg
        
        #Create SVG visuals 
        self.visual_rot(R,vg)
        self.visual_CT(pg,vg)

        return ts.operator(vg_rot, pg)
    
    def projections(self,A):
        tomo_resampled = zoom(self.volume, 
        zoom=(self.Nx/self.volume.shape[0], self.Ny/self.volume.shape[1], self.Nslices/self.volume.shape[2]), 
        order=1)
        projections = A(tomo_resampled)

        return projections

    @staticmethod
    def visual_rot(R,vg):
        ts.svg(R * vg).save("rotation.svg")

    @staticmethod
    def visual_CT(pg,vg):
        P = ts.from_perspective(vol=pg.to_vol())
        ts.svg(P * vg, P * pg).save("CT.svg")
    
    def reconstruction(self,y,A):
        # Prepare preconditioning matrices R and C
        R = 1 / A(np.ones(A.domain_shape))
        R = np.minimum(R, 1 / ts.epsilon)
        C = 1 / A.T(np.ones(A.range_shape))
        C = np.minimum(C, 1 / ts.epsilon)

        # Move all data to GPU:
        dev = torch.device("cuda")
        y = torch.from_numpy(y).to(dev)
        R = torch.from_numpy(R).to(dev)
        C = torch.from_numpy(C).to(dev)
        x_rec = torch.zeros(A.domain_shape, device=dev)

        # Perform algorithm
        start = timer()
        num_iters = 100
        for i in range(num_iters):
            x_rec += C * A.T(R * (y - A(x_rec)))

        # Convert reconstruction back to numpy array
        x_rec = x_rec.cpu().numpy()
        print(f"SIRT finished in {timer() - start:0.2f} seconds using PyTorch")
        return x_rec

    def save_projections(self,folder,projections):
            if not isdir(folder):
                mkdir(folder)
            projections /= np.max(projections) #normalization, not sure if i need to do it here or after ?
            projections = np.round(projections * 65535).astype(np.uint16)
            for i in range(projections.shape[1]):
                projection = projections[:, i, :]
                if i ==0: 
                    print(projection.shape)
                tifffile.imwrite(join(folder, 'proj%04d.tif' % i),projection, compression='zlib') 

    def save_reconstruction(self,folder,reconstruction):
            if not isdir(folder):
                mkdir(folder)
            reconstruction[reconstruction < 0] = 0 #Unsure if you should do this here ?
            reconstruction /= np.max(reconstruction)
            reconstruction = np.round(reconstruction * 255).astype(np.uint8)
            for i in range(reconstruction.shape[2]):
                im = reconstruction[:, :, i]
                #im = np.flipud(im)
                tifffile.imwrite(join(folder, 'reco%04d.tif' % i),im,compression='zlib')