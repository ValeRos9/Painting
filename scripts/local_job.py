import pickle
import socket
import struct
import threading

from Classes.GUI import User_interface
from Classes.mu import Attenuation


REMOTE_HOST = "carbonite"
PORT = 5000


# ---------- Communication helpers ----------

def send_msg(sock, obj):
    data = pickle.dumps(obj)
    sock.sendall(struct.pack(">Q", len(data)) + data)


def recv_msg(sock):
    def recv_all(n):
        data = b""
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    size = struct.unpack(">Q", recv_all(8))[0]
    return pickle.loads(recv_all(size))


# ---------- Remote call ----------

def call_remote(params):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((REMOTE_HOST, PORT))
        send_msg(s, params)
        return recv_msg(s)


# ---------- GUI logic ----------

def run_logic(params):
    # Compute locally
    mu = Attenuation(params['E'], params['symb']).value()
    params['sphere_val'] = mu

    print("mu:", mu)

    def worker():
        try:
            result = call_remote(params)
            print("Received projections:")
            print(result)
        except Exception as e:
            print("Remote error:", e)

    threading.Thread(target=worker, daemon=True).start()


# ---------- Entry point ----------

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