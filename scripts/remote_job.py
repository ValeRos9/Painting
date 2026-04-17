import sys, pickle

from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography

# 1. Lecture des params depuis le flux SSH (stdin)
params = pickle.loads(sys.stdin.buffer.read())

# 2. Calculs
painting = Painting_generator(params['dim_x'], params['dim_y'], params['thickness'],
    params['layers_val'], params['N_spheres'], params['radius'], params['sphere_val']).paint()

proj_geom = Geometry(painting, params['SO'], params['OD'], params['n_proj'], params['geometry_type'],
    params['det_x'], params['det_y'], params['spacing_x'], params['spacing_y']).projection()

tomo = Tomography(painting, proj_geom, params['algorithm'])
projections = tomo.project()

# (Optionnel) Sauvegarde locale sur le serveur pour archivage
tomo.save_projections('projections', projections)
tomo.save_reconstruction('slices', tomo.reconstruct(projections))

# 3. Renvoi du résultat au client via le flux SSH (stdout)
pickle.dump(projections[0], sys.stdout.buffer)
