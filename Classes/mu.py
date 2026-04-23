import xraylib as xray
import periodictable as ptable
import chemparse as chp

#Resources:
#Formula https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html
#code https://github.com/tschoonj/xraylib/wiki/The-xraylib-API-list-of-all-functions#cross-sections

class Attenuation: 
    def __init__(self,E):
        self.energy = E

    def value(self,string=None):
        if string == pigment
            return formula_to_mu(pigment,self.E)
        elif string == "oil":
            self.oil()
        else string == "wood":
            self.wood()

    @staticmethod 
    def formula_to_mu(molecule,E):
        atoms = chp.parse_formula(molecule)
        total_mass = sum(count*getattr(ptable, atom).mass for atom,count in atoms.items())
        amount = 0

        for atom, count in atoms.items():
            element = getattr(ptable, atom)
            wi = count*element.mass
            amount += wi * xray.CS_Total(element.number, E) 

        return amount/total_mass
    
    @staticmethod
    def oil(E):
        chem_comp = {"C18H30O2":0.519, "C18H34O2":0.185, "C18H32O2": 0.142, "C16H32O2":0.07, "C18H36O2":0.034}
        #α-Linolenic acid (51.9–55.2%), "oleic acid": (18.5–22.6%),linoleic acid:14.2–17%, palmitic acid: 7%, stearic acid:3.4%
        total_mu_rho = 0

        for formula,percentage in chem_comp.items():
            mu_rho_compound = Attenuation.formula_to_mu(formula,E)
            total_mu_rho += percentage * mu_rho_compound

        return total_mu_rho
    
    @staticmethod
    def wood(E):
        el_comp = {"C": 0.50, "O": 0.43, "H": 0.06, "N": 0.01}

        total_mu_rho = 0
        for element_symbol, wi in el_comp.items():
            element = getattr(ptable, element_symbol)
            mu_rho_element = xray.CS_Total(element.number, E)
            total_mu_rho += wi * mu_rho_element
        return total_mu_rho


    def formula_to_mu(molecule,E):
        atoms = chp.parse_formula(molecule)
        total_mass = sum(count*getattr(ptable, atom).mass for atom,count in atoms.items())
        amount = 0

        for atom, count in atoms.items():
            element = getattr(ptable, atom)
            wi = count*element.mass
            amount += wi * xray.CS_Total(element.number, E) 

        return amount/total_mass


