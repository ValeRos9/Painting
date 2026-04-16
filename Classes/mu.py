import xraylib as xray
import periodictable as ptable

#Resources:
#Formula https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html
#code https://github.com/tschoonj/xraylib/wiki/The-xraylib-API-list-of-all-functions#cross-sections

class Attenuation: 
    def __init__(self,E,symb):
        self.energy = E
        self.symbol = symb

    def value(self):
        Z = getattr(ptable,self.symbol).number
        mass_attenuation_coefficient = xray.CS_Total(Z, self.energy) 
        #the units of CS_total are cm^2/g which are the units of mu 
        #But is it correct ? does it need to be multiplied by avogadro's number 
        return mass_attenuation_coefficient 


#TD 
#1.Connect to the main code (user inputs of energy and element, does it work ?, connecting this to parameters)
#2.Use linseed oil for the layer_val()