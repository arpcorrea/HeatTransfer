# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:48:19 2021

@author: andre
"""


from .local_fields import RectangularMesh
import numpy as np

class Mesher():
    
    def __init__(self,  problem):
        self.problem = problem
        self.parts = []
        self.interfaces = []
        self.set_domains(problem)
        self.populate_fields_locally(problem)
        self.BC_definition(problem)
        self.dimension_definition( problem)
        self.set_fields(problem)
        self.set_map()
        self.total_nodes(problem)
        self.total_thickness(problem)
        
        
        
        
    def set_domains(self, problem):
        for part in problem.parts:
            self.parts.append(RectangularMesh(part.name))
        for interface in problem.interfaces:
            self.interfaces.append(RectangularMesh(interface.name))


                            
    def populate_fields_locally(self, problem):
        for field_name in problem.required_fields:
            value=0
            value_dict ={}
            extTemp=0
            for part in self.parts:
                for domain in problem.parts:
                    if part.name == domain.name:
                        if field_name == "increments":
                            deltaX = domain.dimensions[0][1] - domain.dimensions[0][0]
                            incX = deltaX/(domain.nodes[0][1] - domain.nodes[0][0])
                            valueX = incX*domain.mask_nodes["All"]
                            value_dict["dx"] = valueX

                            deltaY = domain.dimensions[1][1] - domain.dimensions[1][0]
                            incY = deltaY/(domain.nodes[1][1] - domain.nodes[1][0])
                            valueY = incY*domain.mask_nodes["All"]
                            value_dict["dy"] = valueY
                            part.set_field(field_name, value_dict.copy())
                            
                        elif field_name == "Temperature":
                            value = domain.initial_condition["Temperature"]*domain.mask_nodes["Inner"]
                            # h=np.zeros((problem.totalnodes[1], problem.totalnodes[0]))
                            # Text= np.zeros((problem.totalnodes[1]+2, problem.totalnodes[0]+2))
                            # import pdb; pdb.set_trace()
                            for edge in domain.bc_mask_nodes:
                                # import pdb; pdb.set_trace()
                                for thermal_bc_type in domain.boundary_condition["Thermal"][edge]:
                                    # import pdb; pdb.set_trace()
                                    if thermal_bc_type == "Fixed Temperature":
                                        # import pdb; pdb.set_trace()
                                        value = value+domain.boundary_condition["Thermal"][edge][thermal_bc_type]["Temperature"]*domain.bc_mask_nodes[edge]
                                    if thermal_bc_type == "Convection":
                                        value = value+domain.boundary_condition["Thermal"][edge][thermal_bc_type]["Initial Temperature"]*domain.bc_mask_nodes[edge]
                            part.set_field(field_name, value.copy())
                            # for edge in domain.bc_mask_nodes:
                                
                            # for edge in domain.boundary_condition["Thermal"]:
                                # for kind in domain.boundary_con1dition["Thermal"][edge]:
                                    # if kind == "Fixed Temperature":
                            #             value = value + domain.boundary_condition["Thermal"][edge][kind]["Temperature"]*domain.mask_nodes[edge + " Edge"]
                            #         elif kind == "Convection":
                            #             h = h + domain.boundary_condition["Thermal"][edge][kind]["HTC"]*(domain.mask_nodes[edge + " Edge"]) 
                            #             value = value + domain.boundary_condition["Thermal"][edge][kind]["Initial Temperature"]*domain.mask_nodes[edge + " Edge"]
                            #             Text = Text + domain.boundary_condition["Thermal"][edge][kind]["External Temperature"]*domain.mask_nodes_out[edge + " Edge"]
                            # part.set_field(field_name, value.copy())
                            # part.set_field("Convection Coefficient", h.copy())
                            # part.set_field("External Temperature", Text.copy())
                            
                        elif field_name in domain.material:
                            if isinstance(domain.material[field_name], float):
                                value = domain.material[field_name] * domain.mask_nodes["All"]
                            else:
                                value ={}
                                for var in domain.material[field_name].keys():
                                    value.update({var: domain.material[field_name][var]*domain.mask_nodes["All"] })
                            part.set_field(field_name, value)

                        elif field_name == "Internal Heat Generation":
                            value = np.zeros((problem.totalnodes[1], problem.totalnodes[0]))
                            if bool(domain.power):
                                for location in domain.power:
                                    value = value + domain.power[location]*domain.mask_nodes[location]
                            else:
                                value = value
                            part.set_field(field_name, value)

    def BC_definition(self, problem):
        for part in self.parts:
            for domain in problem.parts:
                if part.name == domain.name:
                    part.set_bc(domain.boundary_condition)

        
        
    def dimension_definition(self, problem):     
        for part in self.parts:
            for domain in problem.parts:
                if part.name == domain.name:
                    part.set_nodes( domain.nodes)
                    part.set_dimensions(domain.dimensions)
        
        
        
    def set_fields(self, problem):
        # import pdb; pdb.set_trace()
        parts = self.parts
        self.global_fields = {}
        
        for field_name in problem.required_fields:
            aux = 0 
            for domain in parts:                
                # import pdb; pdb.set_trace()
                # if field_name not in aux:
                aux= domain.local_fields[field_name]
                # else:
                #     aux = aux + domain.local_fields[field_name]
            self.global_fields.update({field_name: aux})        

        
        
    def set_map(self):
        fields ={}
        self.position = {}
        Ypos = np.zeros(np.shape(self.global_fields["increments"]["dx"])[0]+1)
        Xpos = np.zeros(np.shape(self.global_fields["increments"]["dx"])[1]+1)
        dimY=0
        for i in range (0, np.size(Ypos)-1):
            Ypos[i+1] = Ypos[i] + self.global_fields["increments"]["dy"][i][0]
        for i in range (0, np.size(Xpos)-1):
            Xpos[i+1] = Xpos[i] + self.global_fields["increments"]["dx"][0][i]
        self.position["Y"] = Ypos
        self.position["X"] = Xpos        
        
    def total_nodes(self, problem):
        self.total_nodes = problem.totalnodes

    def total_thickness(self, problem):
        self.total_thickness = problem.thickness
        
        