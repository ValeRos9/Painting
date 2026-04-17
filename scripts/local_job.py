import pickle #new
import subprocess #new 
import threading #new
import os 

from Classes.GUI import User_interface 
from Classes.mu import Attenuation


def run_remote_part(params):

    #Save parameters locally
    with open("params.pkl", "wb") as f:
        pickle.dump(params, f)

    os.system(f"scp params.pkl {USER_HOST}:{REMOTE_DIR}/ && "
              f"ssh {USER_HOST} 'cd {REMOTE_DIR} && PYTHONPATH={REMOTE_DIR} conda run -n Painting python scripts/remote_job.py {REMOTE_DIR}/params.pkl' && "
              f"scp {USER_HOST}:{REMOTE_DIR}/result.pkl .")

    #Load result
    with open("result.pkl", "rb") as f:
        projections = pickle.load(f)
        print(projections)
    print("Simulation executed, projections received!")

#Runs when user clicks "Run" in GUI
def run_logic(params):

    #Compute mu locally
    params['sphere_val'] = Attenuation(params['E'], params['symb']).value()
    print("mu:", params['sphere_val'])

    #Run remote job in background (so GUI doesn't freeze)
    thread = threading.Thread(target=run_remote_part, args=(params,))
    thread.start()

# Start GUI
User_interface(callback=run_logic).run()
