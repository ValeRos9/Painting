import pickle 
import subprocess  
import os 
from Classes.GUI import User_interface 
from Classes.mu import Attenuation


def run_remotely(params):

    #SSH and Remote directory path 
    USER_HOST = "rosariovr@carbonite"
    REMOTE_DIR = "/data/rosariovr/Painting"
    
    with open("params.pkl", "wb") as f:
        pickle.dump(params, f)

    #Upload, Run, Download (Result + SVGs)
    os.system(f"scp params.pkl {USER_HOST}:{REMOTE_DIR}/ && "
              f"ssh {USER_HOST} 'cd {REMOTE_DIR} && PYTHONPATH={REMOTE_DIR} conda run -n tomo_env python scripts/remote_job.py {REMOTE_DIR}/params.pkl' && "
              f"scp {USER_HOST}:{REMOTE_DIR}/result.pkl . && "
              f"scp {USER_HOST}:{REMOTE_DIR}/rotation.svg . && "
              f"scp {USER_HOST}:{REMOTE_DIR}/CT.svg .")

    #Load result
    with open("result.pkl", "rb") as f:
        data = pickle.load(f)

    with open("proj0000.tif", "wb") as f:
        f.write(data)
    print("Simulation executed, projections received!")

    os.system("open -a ImageJ proj0000.tif")
    os.system("open rotation.svg")
    os.system("open CT.svg")

# Start GUI
User_interface(target=run_remotely).run()
