import pickle

from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography


def run_remote(params):
    print("Running on remote GPU server...")

    # 1. Create Painting
    artist = Painting_generator(
        params['dim_x'], params['dim_y'], params['thickness'],
        params['layers_val'], params['N_spheres'],
        params['radius'], params['sphere_val']
    )
    painting = artist.paint()

    # 2. Geometry
    geom = Geometry(
        painting, params['SO'], params['OD'], params['n_proj'],
        params['geometry_type'],
        params['det_x'], params['det_y'],
        params['spacing_x'], params['spacing_y']
    )
    proj_geom = geom.projection()

    # 3. Tomography 
    tomo = Tomography(painting, proj_geom, params['algorithm'])
    """
    projections = tomo.project()
    #slices = Tomo.reconstruct(projections) 

    # 4. Save result (I think it only currently saves projections but doesn't do the reconstruction)
    with open("result.pkl", "wb") as f:
        pickle.dump(projections, f)
        #Tomo.save_projections('projections',projections)
        #Tomo.save_reconstruction('slices',slices)
    """
    print("Remote computation done!")


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "rb") as f:
        params = pickle.load(f)

    run_remote(params)