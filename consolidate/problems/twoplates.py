from .domains import RectangularDomain
from .interfaces import LinearInterface
import numpy as np


class TwoPlates:

    def __init__(self, deck):
        self.set_simulation_parameters(deck)
        self.create_fields(deck)
        self.set_problem_parameters(deck)
        self.set_plates(deck)
        self.set_interfaces(deck)
        
        self.set_material(deck)
        self.set_initial_cond(deck)
        self.set_bc_cond(deck)
        self.set_create_mask(deck)


    def set_simulation_parameters(self,deck):
        self.SimulationParameters = {}
        for par in deck.doc["Simulation"]:
            self.SimulationParameters[par] = deck.doc["Simulation"][par]


    def create_fields(self, deck):
        if deck.doc["Problem Type"]["Type"] == "Welding":
            self.required_fields=["Temperature", "kx", "ky", "Density", "Cp",  "Power Input Heat", "Intimate Contact", "dx","dy","Convection Coefficient", "Interface Temperature"]
        if deck.doc["Problem Type"]["Type"] == "Heat Transfer":
            self.required_fields=["Temperature", "Thermal", "Density", "Power Input Heat", "increments", "Viscosity"]


    def set_problem_parameters(self, deck):
        ny = 0
        thickness = 0
        count = 0
        for domain_name in deck.doc["Domains"]:
            if "Part" in domain_name:
                domain_dir = deck.doc["Domains"][domain_name]
                if count == 0:
                    ny = int((domain_dir["Mesh"]["Points in Y"]))
                    count = count+1
                else:
                    ny = ny + int(domain_dir["Mesh"]["Points in Y"])-1
                nx = int(domain_dir["Mesh"]["Points in X"])
                current_thickness = float(domain_dir["Geometry"]["y1"])
                if current_thickness > thickness:
                    thickness = current_thickness
        self.totalnodes = [nx, ny]
        self.thickness = thickness
        self.length = float(deck.doc["Problem Type"]["Length"])


    def is_top_plate(self,y1,totalthickness):
        return y1 == totalthickness


    def is_bottom_plate(self,y0):
        return y0 == 0


    def set_plates(self, deck):
        self.parts = []
        count=0
        for domain_name in deck.doc["Domains"]:
            if "Part" in domain_name:
                bc ={}
                domain_dir = deck.doc["Domains"][domain_name]
                dimen_x0 = float(domain_dir["Geometry"]["x0"])
                dimen_x1 = float(domain_dir["Geometry"]["x1"])
                dimen_y0 = float(domain_dir["Geometry"]["y0"])
                dimen_y1 = float(domain_dir["Geometry"]["y1"])
                dimen_y0 = float(domain_dir["Geometry"]["y0"])
                dimen_y1 = float(domain_dir["Geometry"]["y1"])
                count=1
                if self.is_bottom_plate(dimen_y0):
                    p_x0 = 0
                    p_x1 = int(deck.doc["Domains"][domain_name]["Mesh"]["Points in X"])-1
                    p_y0 = 0
                    p_y1= int(deck.doc["Domains"][domain_name]["Mesh"]["Points in Y"])-1
                else:
                    aux=0
                    for i in range (1, int(domain_name[-1])):
                        aux = aux +  int(deck.doc["Domains"]["Part " + str(i)]["Mesh"]["Points in Y"])-1
                    p_x0 = 0
                    p_x1 = int(deck.doc["Domains"][domain_name]["Mesh"]["Points in X"])-1*count
                    p_y0 = aux
                    p_y1 = aux + int(deck.doc["Domains"][domain_name]["Mesh"]["Points in Y"])-1*count
                    count=count+1
                nodes=[[p_x0,p_x1],[p_y0, p_y1]]
    
                material={}
                for param in domain_dir["Material Properties"]:
                    if isinstance(domain_dir["Material Properties"][param], str):
                        material[param] = float(domain_dir["Material Properties"][param])
                    else:
                        material[param]={}
                        for aux in domain_dir["Material Properties"][param]:
                            material[param].update({aux: float(domain_dir["Material Properties"][param][aux])})
    
                power = {}
                for cond_name in domain_dir["Initial Condition"]:
                    if cond_name == "Power Input":
                        for location in domain_dir["Initial Condition"]["Power Input"]:
                            power.update({location : float(domain_dir["Initial Condition"]["Power Input"][location])})
                self.parts.append(RectangularDomain(domain_name, dimen_x0, dimen_x1, dimen_y0, dimen_y1, nodes, power))


    def set_interfaces(self, deck):
        self.interfaces =[]
        for domain_name in deck.doc["Domains"]:
            if "Interface" in domain_name:
               self.interfaces.append(LinearInterface(domain_name))



    def set_create_mask(self, deck):
        for i,domain in enumerate(self.parts):
            domain.generate_mask(i,self.totalnodes[1],self.totalnodes[0], self.thickness)
        for interfaces in self.interfaces:
            interfaces.generate_mask(self.parts, self.totalnodes[1],self.totalnodes[0])


    def set_material(self, deck):
        for domain in self.parts:
            material ={}
            domain_dir = deck.doc["Domains"][domain.name]["Material Properties"]
            for param in domain_dir:
                if isinstance(domain_dir[param], str):
                    material[param] = float(domain_dir[param])
                else:
                    material[param]={}
                    for aux in domain_dir[param]:
                        material[param].update({aux: float(domain_dir[param][aux])})
            domain.set_material(material)


    def set_initial_cond(self, deck):
        for domain in self.parts:
            initial_cond ={}
            domain_dir = deck.doc["Domains"][domain.name]["Initial Condition"]
            for cond_name in domain_dir:
                if isinstance(domain_dir[cond_name], str):
                    initial_cond.update({cond_name: float(domain_dir[cond_name])})
                else:
                    initial_cond[cond_name] = {}
                    for location in domain_dir[cond_name]:
                        initial_cond[cond_name].update({location: float(domain_dir[cond_name][location])})
            domain.set_initial_cond(initial_cond)
            
        for interface in self.interfaces:
            initial_cond ={}
            domain_dir = deck.doc["Domains"][interface.name]["Initial Condition"]
            for cond_name in domain_dir:
                if isinstance(domain_dir[cond_name], str):
                    initial_cond.update({cond_name: float(domain_dir[cond_name])})
                else:
                    initial_cond[cond_name] = {}
                    for location in domain_dir[cond_name]:
                        initial_cond[cond_name].update({location: float(domain_dir[cond_name][location])})
            interface.set_initial_cond(initial_cond)

    def set_bc_cond(self, deck):
        for domain in self.parts:
            domain_dir = deck.doc["Domains"][domain.name]["Boundary Condition"]
            bc ={}
            h={}
            for bc_type in domain_dir:
                bc[bc_type]={}
                for kind in domain_dir[bc_type]:
                    bc[bc_type][kind]={}
                    for edge in domain_dir[bc_type][kind]:
                        bc[bc_type][kind][edge]={}
                        for param in domain_dir[bc_type][kind][edge]:
                            bc[bc_type][kind][edge].update({param : float(domain_dir[bc_type][kind][edge][param])})
                            if kind == "Constant Temperature":
                                bc[bc_type][kind][edge].update({"h" : 0})
            domain.set_bc(bc)
            
        for domain in self.interfaces:
            domain_dir = deck.doc["Domains"][domain.name]["Boundary Condition"]
            bc ={}
            h={}
            for bc_type in domain_dir:
                bc[bc_type]={}
                for kind in domain_dir[bc_type]:
                    bc[bc_type][kind]={}
                    for edge in domain_dir[bc_type][kind]:
                        bc[bc_type][kind][edge]={}
                        for param in domain_dir[bc_type][kind][edge]:
                            bc[bc_type][kind][edge].update({param : float(domain_dir[bc_type][kind][edge][param])})
                            if kind == "Constant Temperature":
                                bc[bc_type][kind][edge].update({"h" : 0})
            domain.set_bc(bc)


