# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 11:50:01 2022

@author: acorrea
"""


class LocalMesh():
    
    def __init__(self, domain):
        self.name = domain.name
        self.thermal_BC = domain.bc["Thermal"]
        self.nodes = domain.nodes
        self.dimensions = domain.dimensions

    