import sys, pickle
from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography

if len(sys.argv) < 2: sys.exit("Nom fichier résultat manquant")
res_file = sys.argv[1]

# 1. Lit params depuis le flux (stdin)
try:
    params = pickle.loads(sys.stdin.buffer.read())
except EOFError:
    sys.exit("Aucune donnée reçue")

# 2. Calculs
painting = Painting_generator(params['dim_x'], params['dim_y'], params['thickness'],
    params['layers_val'], params['N_spheres'], params['radius'], params['sphere_val']).paint()

proj_geom = Geometry(painting, params['SO'], params['OD'], params['n_proj'], params['geometry_type'],
    params['det_x'], params['det_y'], params['spacing_x'], params['spacing_y']).projection()

tomo = Tomography(painting, proj_geom, params['algorithm'])
projections = tomo.project()

# Archivage (optionnel)
tomo.save_projections('projections', projections)
tomo.save_reconstruction('slices', tomo.reconstruct(projections))

# 3. Écrit le résultat dans le fichier (pas dans stdout)
with open(res_file, "wb") as f:
    pickle.dump(projections[0], f)
"""
import pickle

from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography


def run_remote(params):
    print("Running on remote GPU server...")

    # 1. Create Painting
    painting = Painting_generator(params['dim_x'], params['dim_y'], params['thickness'],
        params['layers_val'], params['N_spheres'],params['radius'], params['sphere_val']).paint()

    # 2. Generate projection Geometry
    proj_geom = Geometry(painting, params['SO'], params['OD'], params['n_proj'],params['geometry_type'],
        params['det_x'], params['det_y'],params['spacing_x'], params['spacing_y']).projection()

    # 3. Perform projections
    tomo = Tomography(painting, proj_geom, params['algorithm'])
    projections = tomo.project()
    tomo.save_projections('projections',projections)

    #4. Perform reconstructions
    slices = tomo.reconstruct(projections)
    tomo.save_reconstruction('slices',slices)

    # 4. Save result 
    with open("result.pkl", "wb") as f:
        pickle.dump(projections[0], f)
    
    print("Remote computation done!")


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "rb") as f:
        params = pickle.load(f)

    run_remote(params)
"""