import sys
import pickle
from Classes.mu import Attenuation
from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography
import tomosipo as ts 
import torch 


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

def operator(detector,object):
    pixel = 1
    detector_shape
    pg = ts.cone_vec(shape=detector_shape, src_pos=(0,2,0), det_pos=(0,4,0), det_v=(pixel, 0, 0), det_u=(0, 0, pixel),)
    if 
        rot_axis_pos = 
        vg0 = ts.volume(shape=volume_shape, pos=(0, 0, 0), size=volume_shape * voxel_size,)
        R = ts.rotate(pos=rot_axis_pos, axis=(1, 0, 0), angles=angles)
        vg = R * vg0.to_vec()
    else
        vg = ts.volume_vec(*, shape, pos=0, w=(1, 0, 0), v=(0, 1, 0), u=(0, 0, 1))
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
    for i in range(num_iters):
        x_rec += C * A.T(R * (y - A(x_rec)))

    # Convert reconstruction back to numpy array
    x_rec = x_rec.cpu().numpy()
    print(f"SIRT finished in {timer() - start:0.2f} seconds using PyTorch")
    return x_rec


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
#projection
phantom = painting.volume
A = operator()
projections = A(phantom)
reconstructions = reconstruct(projections,A)


#Save projection image at angle 0 
with open("projections/proj0000.tif", "rb") as f:
    data = f.read()

with open("result.pkl", "wb") as f:
    pickle.dump(data, f)
