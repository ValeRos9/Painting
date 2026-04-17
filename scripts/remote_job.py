import socket
import pickle

from Classes.Generator import Painting_generator
from Classes.Geometry import Geometry
from Classes.Tomography import Tomography


PORT = 5000


# ---------- computation ----------

def run_job(params):
    painting = Painting_generator(
        params['dim_x'], params['dim_y'], params['thickness'],
        params['layers_val'], params['N_spheres'],
        params['radius'], params['sphere_val']
    ).paint()

    geom = Geometry(
        painting,
        params['SO'], params['OD'],
        params['n_proj'], params['geometry_type'],
        params['det_x'], params['det_y'],
        params['spacing_x'], params['spacing_y']
    ).projection()

    tomo = Tomography(painting, geom, params['algorithm'])
    projections = tomo.project()

    return projections[0]


# ---------- communication ----------

def recv_all(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            return None
        data += chunk
    return data


def recv_msg(sock):
    size = int.from_bytes(sock.recv(8), "big")
    data = recv_all(sock, size)
    return pickle.loads(data)


def send_msg(sock, obj):
    data = pickle.dumps(obj)
    sock.sendall(len(data).to_bytes(8, "big") + data)


# ---------- server loop ----------

def main():
    print("Worker running...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", PORT))
        s.listen()

        while True:
            conn, _ = s.accept()

            try:
                params = recv_msg(conn)
                result = run_job(params)
                send_msg(conn, result)

            except Exception as e:
                print("Error:", e)

            finally:
                conn.close()


# ---------- entry ----------

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