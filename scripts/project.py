import numpy as np
from Classes.GUI import User_interface
from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography
from Classes.mu import Attenuation


def run_logic(params):
    # 1. Input mu
    mu = Attenuation(params['E'], params['symb']).value()
    params['sphere_val'] = mu
    print(mu)
    
    # 2. Create Painting
    artist = Painting_generator(params['dim_x'], params['dim_y'], params['thickness'], params['layers_val'],
        params['N_spheres'], params['radius'], params['sphere_val'])
    painting = artist.paint()

    # 3. Create projection geometry
    geom = Geometry(painting, params['SO'], params['OD'], params['n_proj'], params['geometry_type'],
                    params['det_x'], params['det_y'], params['spacing_x'], params['spacing_y'])
    proj_geom = geom.projection()

    #4. Perform projection and reconstrution 
    Tomo = Tomography(painting, proj_geom, params['algorithm'])
    projections = Tomo.project() #(This doesn't work locally because mac doesn't have GPUs and we want to do sinogpu3d)

    #Tomo.save_projections('projections',projections)
    #slices = Tomo.reconstruct(projections) 
    #Tomo.save_reconstruction('slices',slices)
    print("Simulation executes")


# Start GUI with logic attached
Viewer = User_interface(callback=run_logic)
Viewer.run()


