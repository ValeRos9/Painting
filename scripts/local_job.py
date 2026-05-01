import pickle, os
from Classes.GUI import User_interface

def run_remotely(params):
    USER_HOST = "rosariovr@carbonite"
    REMOTE_DIR = "/data/rosariovr/Painting"
    
    with open("params.pkl", "wb") as f: 
        pickle.dump(params, f)

    # Upload, Run, Download
    os.system(f"scp params.pkl {USER_HOST}:{REMOTE_DIR}/ && "
              f"ssh {USER_HOST} 'cd {REMOTE_DIR} && PYTHONPATH={REMOTE_DIR} conda run -n tomo_env python scripts/remote_job.py {REMOTE_DIR}/params.pkl' && "
              f"scp {USER_HOST}:{REMOTE_DIR}/result.pkl . && "
              f"scp {USER_HOST}:{REMOTE_DIR}/rotation.svg . && "
              f"scp {USER_HOST}:{REMOTE_DIR}/CT.svg .")

    # Unpack dictionary
    with open("result.pkl", "rb") as f: 
        data = pickle.load(f)
    
    with open("proj0000.tif", "wb") as f: 
        f.write(data["tiff"])

    if data.get("rotation_svg"): 
        with open("rotation.svg", "wb") as f: 
            f.write(data["rotation_svg"])
            
    if data.get("ct_svg"): 
        with open("CT.svg", "wb") as f: 
            f.write(data["ct_svg"])

    os.system("open -a ImageJ proj0000.tif")
    os.system("open rotation.svg")
    os.system("open CT.svg")

User_interface(target=run_remotely).run()
