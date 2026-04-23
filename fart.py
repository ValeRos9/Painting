import chemparse as chemparse
import pubchempy as pcp


def built_in(material):
    molecules = storage(material)
    for molecules,percentage in molecules.items():
        print(molecules)
        print(pcp.get_compounds("cellulose", 'name'))
        compound = pcp.get_compounds(molecules, 'name')[0]
        formula = compound.molecular_formula
        print(formula)


def storage(string):
    if string == "wood":
        molecules_wood = {"cellulose": 0.45,"hemicellulose": 0.25,"lignin": 0.28}
        #cellulose: 0.45,hemicellulose: 0.25,lignin: 0.28

        return molecules_wood 
    elif string == "oil":
        molecules_oil = {"C18H30O2":0.519, "C18H34O2":0.185, "C18H32O2": 0.142, "C16H32O2":0.07, "C18H36O2":0.034} 
        return molecules_oil  
        #α-Linolenic acid (51.9–55.2%), "oleic acid": (18.5–22.6%),
        #linoleic acid:14.2–17%, palmitic acid: 7%, stearic acid:3.4%
    else:
        return print("error")

built_in("wood")