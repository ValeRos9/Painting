import pickle
import socket
import threading
import subprocess
import time

from Classes.GUI import User_interface
from Classes.mu import Attenuation


REMOTE_HOST = "carbonite"
REMOTE_USER = "rosariovr"
PORT = 5000

REMOTE_CMD = (
    "nohup bash -c '"
    "PYTHONPATH=/data/rosariovr/Painting "
    "conda run -n Painting "
    "python /data/rosariovr/Painting/scripts/remote_worker.py "
    "> /data/rosariovr/Painting/worker.log 2>&1 &'"
)


# ---------- simple remote call ----------

def call_remote(params):
    try:
        return send_and_receive(params)
    except Exception:
        print("Worker not running → starting it...")
        start_worker()
        time.sleep(2)  # give it a moment
        return send_and_receive(params)


def send_and_receive(params):
    data = pickle.dumps(params)

    with socket.create_connection((REMOTE_HOST, PORT), timeout=5) as s:
        # send
        s.sendall(len(data).to_bytes(8, "big") + data)

        # receive
        size = int.from_bytes(s.recv(8), "big")
        result = b""
        while len(result) < size:
            result += s.recv(4096)

    return pickle.loads(result)


# ---------- worker startup ----------

def start_worker():
    subprocess.Popen(["ssh", f"{REMOTE_USER}@{REMOTE_HOST}", REMOTE_CMD])


# ---------- GUI logic ----------

def run_logic(params):
    mu = Attenuation(params['E'], params['symb']).value()
    params['sphere_val'] = mu

    print("mu:", mu)

    def worker():
        try:
            result = call_remote(params)
            print("Received projections:")
            print(result)
        except Exception as e:
            print("Error:", e)

    threading.Thread(target=worker, daemon=True).start()


# ---------- entry ----------

if __name__ == "__main__":
    Viewer = User_interface(callback=run_logic)
    Viewer.run()


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