import tomosipo as ts 
import torch 
import numpy as np
from os import mkdir
from os.path import join, isdir
from timeit import default_timer as timer
import tifffile

#Explantion of Geometries: https://aahendriksen.gitlab.io/tomosipo/topics/geometries.html#topics-geometries
#Example of object being rotated: https://aahendriksen.gitlab.io/tomosipo/intro/lab_frame.html
#TO-DO
#Figure out parallel beam, I think it works 
#Figure out multilayered painting 
#Rewrite Generator 

#Figure out how to implement varying geometries 
#Figure out how to do multiple radius 
#Do reconstructions of ESRF 


class Tomo:

    def __init__(self,volume, beam_type, n_proj,det_row,det_col,SO,OD,spacing_x,spacing_y,scale_slices,scale_xy):
        self.volume = volume.transpose(2, 1, 0) 
        print("It's been flipped",self.volume.shape)
        self.beam_type = beam_type
        self.n_proj = n_proj
        self.det_row = det_row
        self.det_col = det_col
        self.SO = SO
        self.OD = OD
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.scale_slices = scale_slices
        self.scale_xy = scale_xy


    def operator(self):

        #Generate projection and volume geometry 
        pg = self.proj_geometry(self.beam_type,self.det_row,self.det_col,self.SO,self.OD,self.spacing_x,self.spacing_y)

        H, W, D = self.volume.shape[0], self.volume.shape[1], self.volume.shape[2]
        vg = self.vol_geometry(H,W,D,self.scale_slices,self.scale_xy)

        #Create rotation geometry and apply
        axis_direction = (1,0,0)
        R = ts.rotate(pos=(0,0,0), axis=axis_direction, angles=np.linspace(0, 2*np.pi, self.n_proj, endpoint=False))
        vg_rot = R*vg

        #Create SVG visuals 
        self.visuals(pg,vg_rot)

        return ts.operator(vg_rot, pg)
    
    @staticmethod
    def proj_geometry(beam,det_row,det_col,SO,OD,spacing_x,spacing_y):

        #set projection geometry (projections are along z)
        if beam == 'cone':
            pg = ts.cone_vec(shape=(det_row,det_col), src_pos=(0,0,-SO), det_pos=(0,0,OD), 
                det_v=(spacing_x, 0, 0), det_u=(0,spacing_y, 0))
        else:
            pg = ts.parallel_vec(shape=(det_row,det_col), ray_dir=(0,0,1), det_pos=(0,0,OD), 
                det_v=(spacing_x, 0, 0), det_u=(0,spacing_y, 0))

        return pg 

    @staticmethod
    def vol_geometry(H,W,D,scale_slices,scale_xy):

        Nslices = int(scale_slices * H)
        Nx, Nz = int(scale_xy * W), int(scale_xy * D)

        dx = W / Nx
        dy = H / Nslices
        dz = D / Nz

        vg = ts.volume_vec(shape=(Nslices,Nx,Nz),pos=(0,0,0), w=(dx,0,0), v=(0,dy,0), u=(0,0,dz))

        return vg
    

    @staticmethod
    def visuals(pg,vg_rot):
        
        s = ts.scale(0.004)
        align = ts.rotate(pos=(0, 0, 0), axis=(1, 0, 0),angles=[np.pi/2])

        ts.svg(align * s * vg_rot, align * s * pg,  width=1200, height=600).save("rotation.svg")
        

    def projections(self, A):
        vol = self.volume  # (80,40,14)
        roi = np.zeros(A.domain_shape, dtype=vol.dtype)  # (120,60,21)

        # compute offsets (center the object)
        off0 = (roi.shape[0] - vol.shape[0]) // 2
        off1 = (roi.shape[1] - vol.shape[1]) // 2
        off2 = (roi.shape[2] - vol.shape[2]) // 2

        roi[off0:off0+vol.shape[0],off1:off1+vol.shape[1],off2:off2+vol.shape[2]] = vol
        projections = A(roi)
        
        return projections
 
    
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
        print(x_rec.shape)
        print(f"SIRT finished in {timer() - start:0.2f} seconds using PyTorch")
        return x_rec

    def save_projections(self,folder,projections):
            if not isdir(folder):
                mkdir(folder)
            projections /= np.max(projections) #normalization, not sure if i need to do it here or after ?
            projections = np.round(projections * 65535).astype(np.uint16)
            for i in range(projections.shape[1]):
                projection = projections[:, i, :]
                tifffile.imwrite(join(folder, 'proj%04d.tif' % i),projection, compression='zlib') 

    def save_reconstruction(self,folder,reconstruction):
            if not isdir(folder):
                mkdir(folder)
            reconstruction[reconstruction < 0] = 0 #Unsure if you should do this here ?
            reconstruction /= np.max(reconstruction)
            reconstruction = np.round(reconstruction * 255).astype(np.uint8)
            for i in range(reconstruction.shape[0]):
                im = reconstruction[i, :, :]
                tifffile.imwrite(join(folder, 'reco%04d.tif' % i),im,compression='zlib')