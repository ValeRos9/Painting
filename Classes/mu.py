import xraylib as xray
import periodictable as ptable
import chemparse as chemparse
#import pubchempy as pcp

#Resources:
#Formula https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html
#code https://github.com/tschoonj/xraylib/wiki/The-xraylib-API-list-of-all-functions#cross-sections

class Attenuation: 
    def __init__(self,E,symb):
        self.energy = E
        self.symb = symb

    #def value(self):
    #    Z = getattr(ptable,self.symbol).number
    #    mass_attenuation_coefficient = xray.CS_Total(Z, self.energy) 
    #    #the units of CS_total are cm^2/g which are the units of mu 
    #    #But is it correct ? does it need to be multiplied by avogadro's number 
    #    return mass_attenuation_coefficient 

    #convert remote job 
    #Check if it's correct with H20 for example
    #do wood, oil, ground in a separate file that will be called up by this one 
    def value(self):
        #Example: "C6H10O5"
        print(chemparse.parse_formula(self.symb))
        atoms = chemparse.parse_formula(self.symb)[0]
        # Returns: [{'C': 6.0, 'H': 10.0, 'O': 5.0}]

        # Calculate total molecular mass
        total_mass = sum(count * getattr(ptable, symb).mass for symb, count in atoms.items())
        
        total_mu_rho = 0.0
        for sym, count in atoms.items():
            element = getattr(ptable, symb)
            # Calculate weight fraction (w_i)
            w_i = (count * element.mass) / total_mass
            # Get mass attenuation coefficient for element
            mu_rho_i = xray.CS_Total(element.number, self.E)
            total_mu_rho += w_i * mu_rho_i
        
        return total_mu_rho

""""
    #Use some computation to figure out the value of wood, oil and ground then store it in some additional file that people can check
    #1. Find those values and replace library by simply a dictionary with wood:mu_wood and oil:mu_oil and so forth
    #2. You can store the step by step in another file  

    @staticmethod
    def library():
        wood = {
            "cellulose": 0.45,
            "hemicellulose": 0.25,
            "lignin": 0.28,
            }

            compound = pcp.get_compounds(keyword_material, 'name')[0]
            formula = compound.molecular_formula



        
        ground = {

        }
        oil = {
            "alpha-linolenic acid": (51.9–55.2%),
            "monounsaturated oleic acid": (18.5–22.6%), 
            The triply unsaturated α-linolenic acid (51.9–55.2%),
The saturated acids palmitic acid (about 7%) and stearic acid (3.4–4.6%),
The monounsaturated oleic acid (18.5–22.6%),
The doubly unsaturated linoleic acid (14.2–17%).
        }



        return


    def value(self):
        Z = getattr(ptable,self.symbol).number
        mass_attenuation_coefficient = xray.CS_Total(Z, self.energy) 
        #the units of CS_total are cm^2/g which are the units of mu 
        #But is it correct ? does it need to be multiplied by avogadro's number 
        return mass_attenuation_coefficient 


TD 
1.Connect to the main code (user inputs of energy and element, does it work ?, connecting this to parameters)
2.Use linseed oil for the layer_val()
"""