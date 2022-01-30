# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:07:54 2021

@author: andre
"""
import numpy as np

class LinearInterface:
    def __init__(self, name):
        self.name = name
        self.initial_condition = {}
        self.boundary_condition = {}


    def set_initial_cond(self, init_cond):
        self.initial_condition.update(init_cond)
        
    def set_bc(self, bc):
        self.boundary_condition.update(bc)
        
    def set_field(self, field_name, value):
        self.local_fields.update({field_name: value})

    def test_grid_interface_inner(self,mesh,domain):
        if mesh[0] ==  domain.nodes[1][1]  and mesh[1] >= domain.nodes[0][0] +1 and mesh[1]<= domain.nodes[0][1] -1:
            return True
        else:
             return False
    def test_grid_interface_all(self,mesh,domain):
        if mesh[0] ==  domain.nodes[1][1]  and mesh[1] >= domain.nodes[0][0] and mesh[1]<= domain.nodes[0][1]:
            return True
        else:
             return False


    def generate_mask(self, domains, totalpy, totalpx):
        self.mask_nodes = {}
        self.mask_nodes_out ={}

        int_num = int(self.name.split()[1])
        mnodes = np.zeros((totalpy, totalpx))
        mnodes_inner = mnodes.copy()
        mnodes_right = mnodes.copy()
        mnodes_left = mnodes.copy()
        mnodes_all = mnodes.copy()

        mnodes_out = np.zeros((totalpy+2, totalpx+2))

        for domain in domains:
            if str(int_num) in domain.name:
                for x_i in range (0,np.shape(mnodes)[0]):
                    for y_i in range (0,np.shape(mnodes)[1]):
                        if self.test_grid_interface_all((x_i, y_i),domain):
                            mnodes_all[x_i][y_i] = 1
                        if self.test_grid_interface_inner((x_i, y_i),domain):
                            mnodes_inner[x_i][y_i] = 1
                            mnodes_right[x_i][-1] = 1
                            mnodes_left[x_i][0] = 1

        self.mask_nodes["All"] = mnodes_all.copy()
        self.mask_nodes["Inner"] = mnodes_inner.copy()
        self.mask_nodes["Left Edge"] = mnodes_left.copy()
        self.mask_nodes["Right Edge"] = mnodes_right.copy()

        self.mask_nodes_out["Left Edge"] = mnodes_out.copy()
        self.mask_nodes_out["Left Edge"][1:-1, :-2] = mnodes_left.copy()
        self.mask_nodes_out["Right Edge"] = mnodes_out.copy()
        self.mask_nodes_out["Right Edge"] [1:-1, 2:] = mnodes_right.copy()