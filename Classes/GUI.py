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
        s1.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        s2.pack(side="left", fill="both", expand=True, padx=10, pady=10)


        f1 = [
            ("Energy [keV]", "E", "100"),
            ("Height []", "height", "80"), ("Width []", "width", "40"),
            ("Layer Type", "type", "['P1']"),
            ("Thickness[]", "thickness", "[10]"),
            ("Pigment", "pigment", "{'P1': ['PbCO3']}"),
            ("N Spheres", "N_spheres", "{'P1':[3]}"),
            ("Radius []", "radius", "{'P1':[2]}"),
        ]

        f2 = [
            ("SO []", "SO", "1000"), ("OD []", "OD", "200"),
            ("N Projections", "n_proj", "180"),
            ("Det X []", "det_x", "256"), ("Det Y []", "det_y", "256"),
            ("Spacing X []", "spacing_x", "1.0"), ("Spacing Y []", "spacing_y", "1.0"),
            ("Beam_type","beam_type","'cone'"),
            ("Scale_xy","scale_xy","1.5"),("Scale_slices","scale_slices","1.5")
        ]

        for i, (label, key, default) in enumerate(f1):
            ttk.Label(s1, text=label, width=15, anchor="e").grid(row=i, column=0, padx=5, pady=5)
            e = ttk.Entry(s1, width=15)
            e.insert(0, default)
            e.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = e

        for i, (label, key, default) in enumerate(f2):
            ttk.Label(s2, text=label, width=15, anchor="e").grid(row=i, column=0, padx=5, pady=5)
            e = ttk.Entry(s2, width=15)
            e.insert(0, default)
            e.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = e

        ttk.Button(self.root, text="Run", command=self._execute).pack(pady=20, fill="x", padx=20)
        ttk.Button(self.root, text="Close", command=self.root.destroy).pack(fill="x", padx=20)

    def _get_params(self):
        p = self.entries
        return {
            key: ast.literal_eval(value.get())
            for key, value in p.items()
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