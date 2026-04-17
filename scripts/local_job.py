import pickle, subprocess, threading, os, time
from Classes.GUI import User_interface 
from Classes.mu import Attenuation

USER, HOST, PATH = "rosariovr", "carbonite", "/data/rosariovr/Painting"
CMD = f"cd {PATH} && PYTHONPATH={PATH} conda run -n Painting python scripts/remote_job.py"

def run_remote(params):
    res_file = f"res_{int(time.time())}.pkl"  # Nom unique
    try:
        # 1. Lance SSH : envoie params (stdin), ignore les bannières (stdout=DEVNULL)
        cmd_ssh = ["ssh", "-T", f"{USER}@{HOST}", CMD, res_file]
        proc = subprocess.Popen(cmd_ssh, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        _, err = proc.communicate(input=pickle.dumps(params))
        
        if proc.returncode != 0: raise Exception(err.decode()[:100])

        # 2. Récupère le fichier résultat et nettoie
        subprocess.run(["scp", "-q", f"{USER}@{HOST}:{PATH}/{res_file}", "."], check=True)
        with open(res_file, "rb") as f: data = pickle.load(f)
        print("Succès ! Projections reçues.")
        
        os.remove(res_file) # Nettoie local
    except Exception as e:
        print(f"Échec: {e}")
    finally:
        # Nettoie distant (silencieux)
        subprocess.run(["ssh", "-T", f"{USER}@{HOST}", "rm", "-f", f"{PATH}/{res_file}"], capture_output=True)

def run_logic(p):
    p['sphere_val'] = Attenuation(p['E'], p['symb']).value()
    threading.Thread(target=run_remote, args=(p,)).start()

if __name__ == "__main__":
    User_interface(callback=run_logic).run()

"""
import numpy as np
import pickle #new
import subprocess #new 
import threading #new

from Classes.GUI import User_interface 
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
    f"{REMOTE_USER}@{REMOTE_HOST}:/data/rosariovr/Painting/"
    ])

    # 3. Run remote script
    subprocess.run([
    "ssh", f"{REMOTE_USER}@{REMOTE_HOST}",
    "cd /data/rosariovr/Painting && PYTHONPATH=/data/rosariovr/Painting conda run -n Painting python scripts/remote_job.py /data/rosariovr/Painting/params.pkl"
    ])

    # 4. Get results back
    subprocess.run([
        "scp",
        f"{REMOTE_USER}@{REMOTE_HOST}:/data/rosariovr/Painting/result.pkl",
        "."
    ])

    # 5. Load result
    with open("result.pkl", "rb") as f:
        projections = pickle.load(f)
        print(projections)
    print("Simulation executed, projections received!")


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
"""