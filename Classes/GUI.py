import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class User_interface:
    def __init__(self, callback=None):
        self.callback = callback  # Store the logic function
        self.root = tk.Tk()
        self.root.title("Parameters")
        self.root.geometry("400x800")
        self.entries = {}

        fields = [
            ("Energy []", "E", 100), ("Symbol", "symb", "Pb"),
            ("Dim X []", "dim_x", 100), ("Dim Y []", "dim_y", 100),
            ("Thickness []", "thickness", "10"), ("N Spheres", "N_spheres", 10), ("Radius []", "radius", 1), 
            ("SO []", "SO", 1000), ("OD []", "OD", 200), ("N Projections", "n_proj", 180),
            ("Det X []", "det_x", 1024), ("Det Y []", "det_y", 1024),
            ("Spacing X []", "spacing_x", 1.0), ("Spacing Y []", "spacing_y", 1.0),
            ("Geometry Type", "geometry_type", "cone"), ("Recon Method", "algorithm", "FDK_CUDA")
        ]

        for label, key, default in fields:
            frm = ttk.Frame(self.root); frm.pack(fill="x", padx=20, pady=5)
            ttk.Label(frm, text=label, width=15, anchor="e").pack(side="left", padx=(0, 10))
            ent = ttk.Entry(frm); ent.insert(0, str(default)); ent.pack(side="left", fill="x", expand=True)
            self.entries[key] = ent

        ttk.Button(self.root, text="Run", command=self._execute).pack(pady=20, fill="x", padx=20)
        ttk.Button(self.root, text="Close", command=self.root.destroy).pack(padx=20, fill="x")

    def _get_params(self):
        p = self.entries
        return {
            'E': int(p['E'].get()), 'symb': str(p['symb'].get()),
            'dim_x': int(p['dim_x'].get()), 'dim_y': int(p['dim_y'].get()),
            'thickness': np.array([int(x) for x in p['thickness'].get().split(',')]),
            'N_spheres': int(p['N_spheres'].get()), 'radius': int(p['radius'].get()), 
            'SO': float(p['SO'].get()), 'OD': float(p['OD'].get()), 'n_proj': int(p['n_proj'].get()),
            'det_x': int(p['det_x'].get()), 'det_y': int(p['det_y'].get()),
            'spacing_x': float(p['spacing_x'].get()), 'spacing_y': float(p['spacing_y'].get()),
            'geometry_type': str(p['geometry_type'].get()), 'algorithm': str(p['algorithm'].get())
        }

    def _execute(self):
        try:
            params = self._get_params()
            if self.callback:
                self.callback(params)  # Run your project.py logic here
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()


#Alternative Ways:
#Modern UI/Complex Interactions: If you need interactive 3D previews of the geometry inside the GUI before running, 
#PyQt6 or PySide6 offers more powerful canvas widgets, though the learning curve is steeper.
#Data Science Workflow: If the primary goal is tweaking parameters and immediately plotting results, 
#Jupyter Widgets (ipywidgets) inside a Notebook might be faster to prototype.