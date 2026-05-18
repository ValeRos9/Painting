import sys, pickle
from Classes.Generator import Painting_generator
from CT_tomosipo import Tomo

def safe_read(path):
        with open(path, "rb") as f:
            return f.read()

# Load params
with open(sys.argv[1], "rb") as f: 
    p = pickle.load(f)

print("Running on remote GPU server...")

# Create Painting
painting = Painting_generator(p['E'], p['type'],p['pigment'], p['height'], p['width'], 
                              p['thickness'], p['N_spheres'], p['radius']).paint()

print("Shape of the painting",painting.volume)
print("Shape of the painting",painting.volume.shape)


# Perform CT (Triggers SVG generation inside Tomo.operator)
CT_tomosipo = Tomo(painting.volume, p['beam_type'], p['n_proj'], p['det_x'], p['det_y'],
    p['SO'], p['OD'], p['spacing_x'], p['spacing_y'], p['scale_slices'], p['scale_xy'])
A = CT_tomosipo.operator() 

projections = CT_tomosipo.projections(A)
CT_tomosipo.save_projections('projections', projections)

slices = CT_tomosipo.reconstruction(projections, A)
CT_tomosipo.save_reconstruction('slices', slices)

# Package & Send (Safe read: handles missing files gracefully)
result_package = {
    "tiff": safe_read("projections/proj0000.tif"),
    "rotation_svg": safe_read("rotation.svg"),
}

with open("result.pkl", "wb") as f:
    pickle.dump(result_package, f)


