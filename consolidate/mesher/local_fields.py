# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:03:59 2021

@author: andre
"""


class RectangularMesh():
    
    def __init__(self, name):
        self.name = name
        self.local_fields = {}
        
        
        
    def set_field(self, field_name, value):
        self.local_fields.update({field_name: value})