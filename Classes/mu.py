
import xraylib as xray
import periodictable as ptable
import chemparse as chp
from functools import lru_cache

#Resources:
#Formula https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html
#code https://github.com/tschoonj/xraylib/wiki/The-xraylib-API-list-of-all-functions#cross-sections



class Attenuation:
    std_materials = {
        "W": {"C": 0.50, "O": 0.43, "H": 0.06, "N": 0.01},
        "O": {"C18H30O2": 0.519,"C18H34O2": 0.185,"C18H32O2": 0.142,
        "C16H32O2": 0.07,"C18H36O2": 0.034,},
    }

    def __init__(self, E):
        self.E = E

    def value(self, keyword):
        materials = self.std_materials.get(keyword)
        if materials:
            return self.mu_rho_default(materials)
        return self.mu_rho_molecule(keyword)

    def mu_rho_default(self, composition):
        """Generic weighted mixture (elements or molecules)."""

        mu_rho = 0
        for comp, weight in composition.items():
            if any(c.isdigit() for c in comp):
                mu_rho += weight * self.mu_rho_molecule(comp)
            else:
                mu_rho += weight * self.cs_total(getattr(ptable, comp).number, self.E)
                
        return mu_rho

    def mu_rho_molecule(self, molecule):
        atoms = chp.parse_formula(molecule)
        total_mass = 0.0
        weighted_sum = 0.0

        for atom, count in atoms.items():
            element = getattr(ptable, atom)
            mass = count * element.mass
            weighted_sum += mass * self.cs_total(element.number, self.E)
            total_mass += mass

        return weighted_sum / total_mass

    @staticmethod
    @lru_cache(maxsize=None)
    def cs_total(Z, E):
        """Cache expensive cross-section calls."""
        return xray.CS_Total(Z, E)