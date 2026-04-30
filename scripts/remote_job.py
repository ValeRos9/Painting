import sys
import pickle
from Classes.mu import Attenuation
from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography
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


def CT_ASTRA(painting, SO, OD, n_proj,geometry_type,det_x,det_y, spacing_x, spacing_y,algorithm):
    #Generate Projection Geometry
    Geom = Geometry(painting, SO, OD, n_proj,geometry_type,det_x,det_y, spacing_x, spacing_y)
    proj_geom = Geom.projection()

    #Perform Tomography 
    tomo = Tomography(painting, proj_geom, algorithm)
    projections = tomo.project()
    tomo.save_projections('projections',projections)
    slices = tomo.reconstruct(projections)
    tomo.save_reconstruction('slices',slices)

def operator(standard,obj,det_x,det_y):
    pixel = 1
    detector_shape = (det_x,det_y)
    s_pos = (0,0,0)
    d_pos = (0,4,0)
    pg = ts.cone_vec(shape=detector_shape, src_pos=s_pos, det_pos=d_pos, det_v=(pixel, 0, 0), det_u=(0, 0, pixel))
    vol_dim = (obj.shape[0],obj.shape[1],obj.shape[2])
    c_pos = (0,0,0)
    if standard == 'standard':
        vg0 = ts.volume(shape=vol_dim, pos=c_pos, size=(1,1,1))
        R = ts.rotate(pos=(0,0,0), axis=(1, 0, 0), angles=np.linspace(0, 2*np.pi, 180, endpoint=False))
        vg = R * vg0.to_vec()
    else:
        vg = ts.volume_vec(vol_dim, pos=c_pos, w=array([[1., 0., 0.]]), v=array([[0., 1., 0.]]), u=array([[0., 0., 1.]]))
    return ts.operator(vg, pg)

    
def reconstruction(y,A):
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

def save_projections(folder,projections):
        if not isdir(folder):
            mkdir(folder)
        projections = np.round(projections * 65535).astype(np.uint16)
        for i in range(projections.shape[1]):
            projection = projections[:, i, :]
            with get_writer(join(folder, 'proj%04d.tif' %i)) as writer:
                writer.append_data(projection, {'compress': 9})
    
def save_reconstruction(folder,reconstruction):
        if not isdir(folder):
            mkdir(folder)
        for i in range(reconstruction.shape[0]):
            im = reconstruction[i, :, :]
            im = np.flipud(im)
            imwrite(join(folder, 'reco%04d.png' % i), im)

######## main #######
with open(sys.argv[1], "rb") as f:
    params = pickle.load(f)

#Test to see if we are in the remote 
print("Running on remote GPU server...")

#Create Painting
painting = Painting_generator(params['E'],params['pigment'],params['dim_x'], params['dim_y'], 
    params['layers'], params['N_spheres'],params['radius']).paint()
print(painting.volume.shape)

#Classic tomography with ASTRA 
# CT_ASTRA(painting, params['SO'], params['OD'], params['n_proj'],params['geometry_type'],
#     params['det_x'], params['det_y'],params['spacing_x'], params['spacing_y'],params['algorithm'])

#CT with tomosipo
keyword = 'standard'
A = operator(keyword,painting.volume,params['det_x'], params['det_y'])
projections = A(painting.volume)
print(projections.shape, type(projections[0]))
#save_projections('projections',projections)
reconstructions = reconstruction(projections,A)
print(reconstructions.shape)


#Save projection image at angle 0 
with open("projections/proj0000.tif", "rb") as f:
    data = f.read()

with open("result.pkl", "wb") as f:
    pickle.dump(data, f)
