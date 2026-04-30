import tomosipo as ts 
import torch 
import numpy as np
from os import mkdir
from os.path import join, isdir
from imageio import get_writer, imwrite
from timeit import default_timer as timer

#Explantion of Geometries: https://aahendriksen.gitlab.io/tomosipo/topics/geometries.html#topics-geometries
#Example of object being rotated: https://aahendriksen.gitlab.io/tomosipo/intro/lab_frame.html
#TO-DO
#. We've got tomosipo on the remote, changed remote conda env from Painting to tomo_env
#. Make reconstruction work, saving both projections, reconstructions
#. Figure out SVG and the jupyter notebook
#. create a separate class, within the remote but not locally sthg like this 
#. Figure out how to implement varying geometries 

class Tomo:

    def __init__(self,volume,word,det_x,det_y,):
        self.volume = volume
        self.word = word
        self.det_x = det_x
        self.det_y = det_y

    def operator(self):
        pixel = 1
        detector_shape = (self.det_x,self.det_y)
        s_pos = (0,0,0)
        d_pos = (0,4,0)
        pg = ts.cone_vec(shape=detector_shape, src_pos=s_pos, det_pos=d_pos, det_v=(pixel, 0, 0), det_u=(0, 0, pixel))
        vol_dim = (self.volume.shape[0],self.volume.shape[1],self.volume.shape[2])
        c_pos = (0,0,0)
        if self.word == 'standard':
            vg0 = ts.volume(shape=vol_dim, pos=c_pos, size=(1,1,1))
            R = ts.rotate(pos=(0,0,0), axis=(1, 0, 0), angles=np.linspace(0, 2*np.pi, 180, endpoint=False))
            vg = R * vg0.to_vec()
        else:
            vg = ts.volume_vec(vol_dim, pos=c_pos, w=array([[1., 0., 0.]]), v=array([[0., 1., 0.]]), u=array([[0., 0., 1.]]))
        return ts.operator(vg, pg)
    
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