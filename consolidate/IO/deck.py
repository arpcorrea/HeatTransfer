# -*- coding: utf-8 -*-
import yaml, sys
import os.path

class Deck():

    def __init__(self, inputhpath):
        if not os.path.exists(inputhpath):
            print("File " + inputhpath)
            sys.exit(1)
        else:
            with open(inputhpath,'r') as f:
                ## Container of the tags parsed from the yaml file
                self.doc = yaml.load(f, Loader=yaml.BaseLoader)
        self.create_folder_structure()
        
        
    def create_folder_structure(self):
        self.plot_dirTemp = self.doc["Plot"]["Temp Output Folder"]
        check_folder_Temp = os.path.isdir(self.plot_dirTemp)
        if not check_folder_Temp:
              os.makedirs(self.plot_dirTemp)