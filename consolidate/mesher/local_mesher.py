# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:48:19 2021

@author: andre
"""


from .local_fields import RectangularMesh
import numpy as np

class LocalMesher():
    
    def __init__(self,  problem):
        self.problem = problem
        self.parts = []
        self.interfaces = []
        self.set_domains(problem)
        self.populate_fields_locally(problem)
        
        
        
    def set_field(self, field_name, value):
        self.local_fields.update({field_name: value})
        
        
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
                            valueX = incX*domain.mask_inter_nodes["All"]
                            value_dict["dx"] = valueX

                            deltaY = domain.dimensions[1][1] - domain.dimensions[1][0]
                            incY = deltaY/(domain.nodes[1][1] - domain.nodes[1][0])
                            valueY = incY*domain.mask_inter_nodes["All"]
                            value_dict["dy"] = valueY
                            part.set_field(field_name, value_dict.copy())
                            
                        elif field_name == "Temperature":
                            value = domain.initial_condition["Temperature"]*domain.mask_nodes["Inner"]
                            h=np.zeros((problem.totalnodes[1], problem.totalnodes[0]))
                            Text= np.zeros((problem.totalnodes[1]+2, problem.totalnodes[0]+2))
                            for kind in domain.boundary_condition["Thermal"]:
                                for edge in domain.boundary_condition["Thermal"][kind]:
                                    value = value + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_nodes[edge]
                                    if kind == "Fixed Boundary":
                                        h=h
                                        Text = Text + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_nodes_out[edge]
                                    elif kind == "Convection":
                                        h = h + domain.boundary_condition["Thermal"][kind][edge]["Convection Coefficient"]*(domain.mask_nodes[edge]) 
                                        value = value + domain.initial_condition["Temperature"]*domain.mask_nodes[edge]
                                        Text = Text + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_nodes_out[edge]
                            part.set_field(field_name, value.copy())
                            part.set_field("Convection Coefficient", h.copy())
                            part.set_field("External Temperature", Text.copy())
                            
                        elif field_name in domain.material:
                            if isinstance(domain.material[field_name], float):
                                value = domain.material[field_name] * domain.mask_inter_nodes["All"]
                            else:
                                value ={}
                                for var in domain.material[field_name].keys():
                                    value.update({var: domain.material[field_name][var]*domain.mask_inter_nodes["All"] })
                            part.set_field(field_name, value)

                        elif field_name == "Power Input Heat":
                            value = np.zeros((problem.totalnodes[1], problem.totalnodes[0]))
                            if bool(domain.power):
                                for location in domain.power:
                                    value = value + domain.power[location]*domain.mask_nodes[location]
                            else:
                                value = value
                            part.set_field(field_name, value)

            for interface in self.interfaces:
                for domain in problem.interfaces:
                    if interface.name == domain.name:
                        if field_name == "Temperature":
                            value = domain.initial_condition["Temperature"]*domain.mask_nodes["Inner"]
                            h=np.zeros((problem.totalnodes[1], problem.totalnodes[0]))
                            Text= np.zeros((problem.totalnodes[1]+2, problem.totalnodes[0]+2))
                            for kind in domain.boundary_condition["Thermal"]:
                                for edge in domain.boundary_condition["Thermal"][kind]:
                                    value = value + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_nodes[edge]
                                    if kind == "Fixed Boundary":
                                        h=h
                                        Text = Text + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_nodes_out[edge]
                                    elif kind == "Convection":
                                        h = h + domain.boundary_condition["Thermal"][kind][edge]["Convection Coefficient"]*(domain.mask_nodes[edge]) 
                                        value = value + domain.initial_condition["Temperature"]*domain.mask_nodes[edge]
                                        Text = Text + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_nodes_out[edge]
                            interface.set_field(field_name, value.copy())
                            interface.set_field("Convection Coefficient", h.copy())
                            interface.set_field("External Temperature", Text.copy())

                    if field_name == "Roughness":
                        value ={}
                        for var in domain.initial_condition["Roughness"]:
                            value.update({var: domain.initial_condition["Roughness"][var]*domain.mask_nodes["All"]})
                        interface.set_field(field_name, value)



    def populate_fields_globally(self, problem):
       value=0
       value_dict ={}
       extTemp=0
       h=np.zeros((problem.totalnodes[1], problem.totalnodes[0]))
       Text= np.zeros((problem.totalnodes[1]+2, problem.totalnodes[0]+2))
       for domain in (problem.parts + problem.interfaces):
            value = value + domain.initial_condition["Temperature"]*domain.mask_nodes["Inner"]
            for kind in domain.boundary_condition["Thermal"]:
                for edge in domain.boundary_condition["Thermal"][kind]:
                    value = value + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_nodes[edge]
                    if kind == "Fixed Boundary":
                        h=h
                        Text = Text + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_nodes_out[edge]
                    if kind == "Convection":
                        h = h + domain.boundary_condition["Thermal"][kind][edge]["Convection Coefficient"]*(domain.mask_nodes[edge]) 
                        value = value + domain.initial_condition["Temperature"]*domain.mask_nodes[edge]
                        Text = Text + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_nodes_out[edge]

       self.set_field("Temperature", value)
       self.set_field("Convection Coefficient", h)
       self.set_field("External Temperature", Text)
       
       for field_name in problem.required_fields:
            value=0
            value_dict2 ={}
            extTemp=0
            value_dict["dx"] = 0
            value_dict["dy"] = 0
            for domain in problem.plates:
                if field_name == "increments":
                    deltaX = domain.dimensions[0][1] - domain.dimensions[0][0]
                    incX = deltaX/(domain.nodes[0][1] - domain.nodes[0][0])
                    valueX = incX*domain.mask_inter_nodes["All"]
                    value_dict["dx"] = valueX + value_dict["dx"]
                
                    deltaY = domain.dimensions[1][1] - domain.dimensions[1][0]
                    incY = deltaY/(domain.nodes[1][1] - domain.nodes[1][0])
                    valueY = incY*domain.mask_inter_nodes["All"]
                    value_dict["dy"] = valueY + value_dict["dy"]

                    self.set_field(field_name, value_dict)

                elif field_name in domain.material:
                    if isinstance(domain.material[field_name], float):
                        value = domain.material[field_name] * domain.mask_inter_nodes["All"] + value
                    else:
                        for var in domain.material[field_name].keys():
                            if var in value_dict2:
                                value_dict2[var] = domain.material[field_name][var]*domain.mask_inter_nodes["All"] + value[var]
                            else:
                                value_dict2.update({var: domain.material[field_name][var]*domain.mask_inter_nodes["All"] })
                                value = value_dict2
                    self.set_field(field_name, value)

