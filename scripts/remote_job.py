import pickle
import socket
import struct
import sys

from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography


HOST = "0.0.0.0"
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


# ---------- Core computation ----------

def run_job(params):
    painting = Painting_generator(
        params['dim_x'], params['dim_y'], params['thickness'],
        params['layers_val'], params['N_spheres'],
        params['radius'], params['sphere_val']
    ).paint()

    geom = Geometry(
        painting, params['SO'], params['OD'],
        params['n_proj'], params['geometry_type'],
        params['det_x'], params['det_y'],
        params['spacing_x'], params['spacing_y']
    ).projection()

    tomo = Tomography(painting, geom, params['algorithm'])
    projections = tomo.project()

    return projections[0]


# ---------- Worker loop ----------

def handle_client(conn):
    try:
        params = recv_msg(conn)
        print("Job received", file=sys.stderr)

        result = run_job(params)

        send_msg(conn, result)

    except Exception as e:
        print("Worker error:", e, file=sys.stderr)
    finally:
        conn.close()


def main():
    print(f"Worker listening on port {PORT}", file=sys.stderr)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, _ = s.accept()
            handle_client(conn)


if __name__ == "__main__":
    main()





"""
import pickle

from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography


def run_remote(params):
    print("Running on remote GPU server...")

    # 1. Create Painting
    painting = Painting_generator(params['dim_x'], params['dim_y'], params['thickness'],
        params['layers_val'], params['N_spheres'],params['radius'], params['sphere_val']).paint()

    # 2. Generate projection Geometry
    proj_geom = Geometry(painting, params['SO'], params['OD'], params['n_proj'],params['geometry_type'],
        params['det_x'], params['det_y'],params['spacing_x'], params['spacing_y']).projection()

    # 3. Perform projections
    tomo = Tomography(painting, proj_geom, params['algorithm'])
    projections = tomo.project()
    tomo.save_projections('projections',projections)

    #4. Perform reconstructions
    slices = tomo.reconstruct(projections)
    tomo.save_reconstruction('slices',slices)

    # 4. Save result 
    with open("result.pkl", "wb") as f:
        pickle.dump(projections[0], f)
    
    print("Remote computation done!")


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "rb") as f:
        params = pickle.load(f)

    run_remote(params)
"""