# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:03:59 2021

@author: andre
"""


class RectangularMesh():
    
    def __init__(self, name):
        self.name = name
        self.local_fields = {}
        self.nodes = []
        self.bc= {}
        self.dimensions=[]
        
        
        
    def set_field(self, field_name, value):
        self.local_fields.update({field_name: value})
        
    def set_nodes(self, value):
        self.nodes = value 
        
    def set_dimensions(self, value):
        self.dimensions = value     
    
    def set_bc(self, value):
        self.bc = value