import pickle 
import subprocess  
#import threading 
import os 
from Classes.GUI import User_interface 
from Classes.mu import Attenuation


USER_HOST = "rosariovr@carbonite"
REMOTE_DIR = "/data/rosariovr/Painting"

def run_remotely(params):
    
    with open("params.pkl", "wb") as f:
        pickle.dump(params, f)

    #Condensed execution: Upload, Run, Download
    os.system(f"scp params.pkl {USER_HOST}:{REMOTE_DIR}/ && "
              f"ssh {USER_HOST} 'cd {REMOTE_DIR} && PYTHONPATH={REMOTE_DIR} conda run -n Painting python scripts/remote_job.py {REMOTE_DIR}/params.pkl' && "
              f"scp {USER_HOST}:{REMOTE_DIR}/result.pkl .")

    #Load result
    with open("result.pkl", "rb") as f:
        data = pickle.load(f)

    with open("proj0000.tif", "wb") as f:
        f.write(data)
    print("Simulation executed, projections received!")

    os.system("open -a ImageJ proj0000.tif")

# Start GUI
User_interface(target=run_remotely).run()



"""
def run_remote_part(params):
    
    with open("params.pkl", "wb") as f:
        pickle.dump(params, f)

    #Condensed execution: Upload, Run, Download
    os.system(f"scp params.pkl {USER_HOST}:{REMOTE_DIR}/ && "
              f"ssh {USER_HOST} 'cd {REMOTE_DIR} && PYTHONPATH={REMOTE_DIR} conda run -n Painting python scripts/remote_job.py {REMOTE_DIR}/params.pkl' && "
              f"scp {USER_HOST}:{REMOTE_DIR}/result.pkl .")

    #Load result
    with open("result.pkl", "rb") as f:
        data = pickle.load(f)

    with open("proj0000.tif", "wb") as f:
        f.write(data)
    print("Simulation executed, projections received!")

    os.system("open -a ImageJ proj0000.tif")

#Function: that Runs when user clicks "Run" in GUI
def run_logic(params):
    #Run remote job in background (so GUI doesn't freeze)
    thread = threading.Thread(target=run_remote_part, args=(params,))
    thread.start()

# Start GUI
User_interface(callback=run_logic).run()
"""