import xraylib as xray
import periodictable as ptable
import chemparse as chemparse
#import pubchempy as pcp

#Resources:
#Formula https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html
#code https://github.com/tschoonj/xraylib/wiki/The-xraylib-API-list-of-all-functions#cross-sections

class Attenuation: 
    def __init__(self,E,pigment):
        self.energy = E
        self.pigment = pigment

    def value(self):
        atoms = chemparse.parse_formula(self.pigment)
        total_mass = sum(count*getattr(ptable, atom).mass for atom,count in atoms.items())
        amount = 0
        for atom, count in atoms.items():
            element = getattr(ptable, atom)
            wi = count*element.mass
            amount += wi * xray.CS_Total(getattr(ptable, atom).number, self.energy) 
        return amount/total_mass

#You need to compute the mu for wood and oil and then fit everything together in a general manner


    # def mu__wood_or_oil(self):
    #     keyword = wood 
    #     molecules = self.storage(keyword)
    #     summer = 0
    #     for molecules,percentage in wood.items:
    #         compound = pcp.get_compounds(molecules, 'name')[0]
    #         formula = compound.molecular_formula
    #         mu_rho_compound = self.value(formula)
    #         summer += percentage * mu_rho_compound
    #     return summer
    
    # @statimethod
    # def storage(string)
    #     if string == wood
    #         return molecules_wood = {"cellulose": 0.45,"hemicellulose": 0.25,"lignin": 0.28}
    #     elif string == oil 
    #         return molecules_oil = {"C18H30O2":0.519, "C18H34O2":0.185, "C18H32O2": 0.142, "C16H32O2":0.07, "C18H36O2":0.034} 
    #         #α-Linolenic acid (51.9–55.2%), "oleic acid": (18.5–22.6%),
    #         #linoleic acid:14.2–17%, palmitic acid: 7%, stearic acid:3.4%
    #     else 
    #         return print("error")


