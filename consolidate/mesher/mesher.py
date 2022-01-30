# -*- coding: utf-8 -*-
import numpy as np
from .fields import Field

class Mesher():

    def __init__(self, local_mesh):
        self.set_fields(local_mesh)
        self.set_map()

                
    def set_map(self):
        fields ={}
        self.position = {}
        Ypos = np.zeros(np.shape(self.fields["increments"]["dx"])[0]+1)
        Xpos = np.zeros(np.shape(self.fields["increments"]["dx"])[1]+1)
        dimY=0
        for i in range (0, np.size(Ypos)-1):
            Ypos[i+1] = Ypos[i] + self.fields["increments"]["dy"][i][0]
        for i in range (0, np.size(Xpos)-1):
            Xpos[i+1] = Xpos[i] + self.fields["increments"]["dx"][0][i]
        self.position["Y"] = Ypos
        self.position["X"] = Xpos
        
        
    def set_fields(self, local_mesh):
        parts = local_mesh.parts
        interfaces = local_mesh.interfaces
        self.fields = {}
        for field_name in parts[0].local_fields:
            if isinstance (parts[0].local_fields[field_name], dict):
                aux ={}
                for domain in parts:
                    for variable in domain.local_fields[field_name].keys():
                        if variable not in aux:
                            aux[variable] = domain.local_fields[field_name][variable]
                        else:
                            aux[variable] = aux[variable] + domain.local_fields[field_name][variable]
                self.fields.update({field_name: aux})
            else:
                aux=0
                for domain in parts:
                    aux = aux + domain.local_fields[field_name]
                self.fields.update({field_name: aux})
                
        for field_name in interfaces[0].local_fields:
            if isinstance (interfaces[0].local_fields[field_name], dict):
                aux ={}
                for domain in interfaces:
                    for variable in domain.local_fields[field_name].keys():
                        if variable not in aux:
                            aux[variable] = domain.local_fields[field_name][variable]
                        else:
                            aux[variable] = aux[variable] + domain.local_fields[field_name][variable]
                            if field_name in self.fields2:
                                aux[variable] = self.fields2[field_name] + aux[variable]
                self.fields.update({field_name: aux})
            else:
                aux=0
                aux2 = 0
                for domain in interfaces:
                    aux2 = aux2 + domain.local_fields[field_name]
                    if field_name in self.fields:
                        aux = self.fields[field_name] + aux2
                    else:
                        aux = aux2
            self.fields.update({field_name: aux})
            
                
