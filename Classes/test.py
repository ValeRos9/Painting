
def layers(type, thickness, pigment, N_spheres, N_radius):
    layers_dict = {}

    for i in range(len(type)-1):
        layers_dict[type[i]] = {'thickness':thickness[i],'pigment':pigment[str(i+1)],
            'N_spheres':N_spheres[str(i+1)],'radius':N_radius[i]} 
    return layers_dict

layer_type = ['P1','P2','G','W']
thickness = [10,20,30,40]
pigment_type = {'1':['HgS','PbCO3'],'2':['Ag','PbCO3'],'3':['S']}
N_spheres = {'1':[10e4,10e6],'2':[10e5,10e3],'3':[10e2]}
N_radius = [1,2,5,7,10]

layers = layers(layer_type, thickness, pigment_type, N_spheres, N_radius)
print(layers)
for key, qty in layers.items():
    if key.startswith(('P', 'G')):
        print(key)

print(sum(thickness))


    # def paint(self):
    #     """generates a volume, inserts spheres and adds mu values"""

    #     #Create volume
    #     total_thickness = sum(count for count in self.layers.values())
    #     volume = np.empty((total_thickness,self.width,self.height)) 

    #     #Set Painting layers with quantities  
    #     Painting_layers = Layers(self.layer_type, self.thickness,self.pigment, self.N_spheres, self.N_radius)

    #     #Create Attenuation Class
    #     mu = Attenuation(self.E)

    #     i = 0
    #     for layer, qtys in Painting_Layers.items():

    #         if layer.startswith(('P', 'G')):

    #             thickness = qtys['thickness']
    #             volume[i:i+thickness,:,:] = mu.value('O')

    #             for sphere_i in range(len(qtys['N_spheres'])-1):
                    
    #                 if thickness < 2 * self.radius + 1:
    #                     print("Error! thickness of Paint or Ground layer", thickness, "is too small compared with r_sphere=", self.radius,",radius can't be more than",(thickness-1)/2)
    #                     raise SystemExit(1)

    #                 else:
    #                     N_sphere = qtys['N_spheres'][sphere_i]
    #                     N_radius = qtys['N_radius'][sphere_i]
    #                     pigment = qtys['pigment'][sphere_i]
    #                     centers = self.random_insert_spheres(volume[i:i+thickness,:,:], N_sphere, N_radius, mu.value(pigment))
    #         else:

    #             volume[i:i+thickness,:,:]= mu.value(layer)

    #         i += thickness

    #     return Painting(volume)

