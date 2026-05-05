import xraylib as xlib
import periodictable as ptable
import chemparse as chp
from functools import lru_cache

#Resources:
#Formula for mu_rho https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html
#code https://github.com/tschoonj/xraylib/wiki/The-xraylib-API-list-of-all-functions#cross-sections

class Attenuation:
    std_materials = {
        "W": {"C": 0.50, "O": 0.43, "H": 0.06, "N": 0.01},
        "O": {"C18H30O2": 1}, #"O": {"C18H30O2": 0.519,"C18H34O2": 0.185,"C18H32O2": 0.142,"C16H32O2": 0.07,"C18H36O2": 0.034,},
    }

    def __init__(self, E):
        self.E = E

    def value(self, keyword):
        materials = self.std_materials.get(keyword)
        if materials:
            return self.mu_default(materials)
        return self.mu_molecule(keyword)

    def mu_default(self, composition):
        """Generic weighted mixture (elements or molecules)."""

        mu_tot = 0
        for comp, fraction in composition.items():
            if any(c.isdigit() for c in comp):
                mu_tot += fraction * self.mu_molecule(comp)
            else:
                Z = getattr(ptable, comp).number
                mu = xlib.ElementDensity(Z) * self.cs_total(Z, self.E)
                mu_tot += fraction * mu
                
        return mu_tot

    def mu_molecule(self, molecule):
        atoms = chp.parse_formula(molecule)
        total_mass = 0.0
        weighted_sum = 0.0

        for atom, count in atoms.items():
            element = getattr(ptable, atom)
            mass = count * element.mass
            Z = element.number
            mu = xlib.ElementDensity(Z) * self.cs_total(Z, self.E)
            weighted_sum += mass * mu
            total_mass += mass

        return weighted_sum / total_mass

    @staticmethod
    @lru_cache(maxsize=None)
    def cs_total(Z, E):
        """Cache expensive cross-section calls."""
        return xlib.CS_Total(Z, E)
    

    #Fred notes:
    # 1. Linear attenuation coefficient is what you get from an unknown composition reconstruction 
    # mu = [cm^-1]
    # mu/rho * rho = 
    # 3. Ground layer, like painting structure, chalk or lead white or a mixture in linseed oil,
    # with thicker spheres 
    # 4. Canvas -> textile fiber (but what type won't matter much to the CT)
    #paint+groung = 0.5mm, and canvas = 1mm
    # 10^5 x 10^5 x 10^2 microns - 100'000 spheres with radius 1 microns 

    # 10^6 x 10^6 x 10^4 - 100'000 spheres with radius 5 microns 

    # r = 5 microns = 5
    # y = 1 m = 1 x 10 ^6 microns 
    # depth = 1 m = 100 cm
    # 2. Maybe x-ray lib can do it more directly