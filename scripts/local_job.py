import numpy as np
import pickle #new
import subprocess #new 
import threading #new

from Classes.GUI import User_interface #new
from Classes.mu import Attenuation


REMOTE_USER = "rosariovr"
REMOTE_HOST = "carbonite"
REMOTE_PATH = "/data/rosariovr/Painting/scripts"   # same folder where remote_job.py lives


def run_remote_part(params):
    # 1. Save parameters locally
    with open("params.pkl", "wb") as f:
        pickle.dump(params, f)

    # 2. Send params to remote server
    subprocess.run([
        "scp", "params.pkl",
        f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}/"
    ])

    # 3. Run remote script
    subprocess.run([
        "ssh", f"{REMOTE_USER}@{REMOTE_HOST}",
        f"cd /data/rosariovr/Painting && PYTHONPATH=. python3 scripts/remote_job.py params.pkl"
    ])

    # 4. Get results back
    subprocess.run([
        "scp",
        f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}/result.pkl",
        "."
    ])

    # 5. Load result
    with open("result.pkl", "rb") as f:
        projections = pickle.load(f)

    print("Simulation executed, projections received!")

    # 👉 If you want: update GUI here with projections


def run_logic(params):
    # Runs when user clicks "Run" in GUI

    # 1. Compute mu locally
    mu = Attenuation(params['E'], params['symb']).value()
    params['sphere_val'] = mu

    print("mu:", mu)

    # 2. Run remote job in background (so GUI doesn't freeze)
    thread = threading.Thread(target=run_remote_part, args=(params,))
    thread.start()


# Start GUI
Viewer = User_interface(callback=run_logic)
Viewer.run()