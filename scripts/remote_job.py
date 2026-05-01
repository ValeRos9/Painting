import sys, pickle
from Classes.Generator import Painting_generator
from CT_tomosipo import Tomo

def safe_read(path):
        with open(path, "rb") as f:
            return f.read()


# Load params
with open(sys.argv[1], "rb") as f: 
    params = pickle.load(f)

print("Running on remote GPU server...")

# Create Painting
painting = Painting_generator(params['E'], params['pigment'], params['dim_x'], params['dim_y'], 
                              params['layers'], params['N_spheres'], params['radius']).paint()

print(painting.volume.shape)

# CT Setup
n_proj, det_row, det_col = params['n_proj'], params['det_x'], params['det_y']
spacing_x, spacing_y, SO, OD = params['spacing_x'], params['spacing_y'], params['SO'], params['OD']
Nx = 256
Ny = 256 
n_slices = 100

# Perform CT (Triggers SVG generation inside Tomo.operator)
CT_tomosipo = Tomo(painting.volume, n_proj, det_row, det_col, SO, OD, spacing_x, spacing_y, Nx, Ny, n_slices)
A = CT_tomosipo.operator() 

projections = CT_tomosipo.projections(A)
CT_tomosipo.save_projections('projections', projections)

slices = CT_tomosipo.reconstruction(projections, A)
CT_tomosipo.save_reconstruction('slices', slices)

# Package & Send (Safe read: handles missing files gracefully)
result_package = {
    "tiff": safe_read("projections/proj0000.tif"),
    "rotation_svg": safe_read("rotation.svg"),
    "ct_svg": safe_read("CT.svg"),
}

with open("result.pkl", "wb") as f:
    pickle.dump(result_package, f)


