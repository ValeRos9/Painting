import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import threading 
import ast

class User_interface:
    def __init__(self, target=None):
        self.target = target
        self.root = tk.Tk()
        self.root.title("Parameters")
        self.root.geometry("400x800")
        self.entries = {}

        s1 = ttk.LabelFrame(self.root, text="Painting")
        s2 = ttk.LabelFrame(self.root, text="CT")
        s1.pack(fill="x", padx=20, pady=10)
        s2.pack(fill="x", padx=20, pady=10)

        #Alternative for pigment, it is a dictionary (key:layer number,value:list of strings for formulas)
        #{1:PbC03,S3H2,2:NaCL,AuPbC03}
        #Maybe change the name to pigment 
        #You would have to iterate through the list for a given layer 
        #maybe layer_nbr -> pigments = self.pigment[nbr] and iteration for spheres
        #Maybe know you want to generalize with the thickness as well
        #nbr of layers 5 
        #Type {P,P,P,G,W}
        #Thickness 50,60,70,80,90
        #Pigment per P layer 1:PbC03,S3H2,2:NaCL,AuPbC03


        f1 = [
            ("Energy [keV]","E",100),("Pigment","pigment","{'1': ['PbCO3','HgS'], '2': 'PbCO3'}"),
            ("Height []","height",80),("Width []","width",40),
            ("Layers {'type':thickness[]}","layers","{'P': 10, 'G': 2, 'W': 2}"),
            ("N Spheres","N_spheres",10),("Radius []","radius",1)
        ]
        f2 = [
            ("SO []","SO",1000),("OD []","OD",200),("N Projections","n_proj",1),
            ("Det X []","det_x",256),("Det Y []","det_y",256),
            ("Spacing X []","spacing_x",1.0),("Spacing Y []","spacing_y",1.0),
        ]

        for parent, fields in [(s1,f1),(s2,f2)]:
            for label, key, default in fields:
                f = ttk.Frame(parent); f.pack(fill="x", padx=10, pady=5)
                ttk.Label(f, text=label, width=20, anchor="e").pack(side="left", padx=(0,10)) #width change label size
                e = ttk.Entry(f,width=20); e.insert(0,str(default)); e.pack(side="left", fill="x", expand=True) #same for entry
                self.entries[key] = e

        ttk.Button(self.root, text="Run", command=self._execute).pack(pady=20, fill="x", padx=20)
        ttk.Button(self.root, text="Close", command=self.root.destroy).pack(fill="x", padx=20)

    def _get_params(self):
        p = self.entries
        return {
            'E': int(p['E'].get()), 'pigment': ast.literal_eval(p['pigment'].get()),
            'height': int(p['height'].get()), 'width': int(p['width'].get()),
            'layers': ast.literal_eval(p['layers'].get()),
            'N_spheres': int(p['N_spheres'].get()), 'radius': int(p['radius'].get()),
            'SO': float(p['SO'].get()), 'OD': float(p['OD'].get()), 'n_proj': int(p['n_proj'].get()),
            'det_x': int(p['det_x'].get()), 'det_y': int(p['det_y'].get()),
            'spacing_x': float(p['spacing_x'].get()), 'spacing_y': float(p['spacing_y'].get()),
        }

    def _execute(self):
        threading.Thread(target=self.target, args=(self._get_params(),)).start()

    def run(self):
        self.root.mainloop()
    



#Alternative Ways:
#Modern UI/Complex Interactions: If you need interactive 3D previews of the geometry inside the GUI before running, 
#PyQt6 or PySide6 offers more powerful canvas widgets, though the learning curve is steeper.
#Data Science Workflow: If the primary goal is tweaking parameters and immediately plotting results, 
#Jupyter Widgets (ipywidgets) inside a Notebook might be faster to prototype.