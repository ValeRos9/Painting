import pickle, os
from Classes.GUI import User_interface

def run_remotely(params):
    USER_HOST = "rosariovr@carbonite"
    REMOTE_DIR = "/data/rosariovr/Painting"
    
    # Save params
    with open("params.pkl", "wb") as f:
        pickle.dump(params, f)

    # Upload → Run → Download (only result.pkl)
    os.system(
        f"scp params.pkl {USER_HOST}:{REMOTE_DIR}/ && "
        f"ssh {USER_HOST} 'cd {REMOTE_DIR} && "
        f"PYTHONPATH={REMOTE_DIR} conda run -n tomo_env python scripts/remote_job.py {REMOTE_DIR}/params.pkl' && "
        f"scp {USER_HOST}:{REMOTE_DIR}/result.pkl ."
    )

    # Load results
    with open("result.pkl", "rb") as f:
        data = pickle.load(f)

    if data.get("tiff"):
        open("proj0000.tif", "wb").write(data["tiff"])

    if data.get("rotation_svg"):
        open("rotation.svg", "wb").write(data["rotation_svg"])

    if data.get("ct_svg"):
        open("CT.svg", "wb").write(data["ct_svg"])

    os.system("open -a ImageJ proj0000.tif")
    os.system("open rotation.svg")
    os.system("open CT.svg")


User_interface(target=run_remotely).run()