# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 16:36:58 2021

@author: andre
"""


import matplotlib.pyplot as plt
from PIL import Image
import glob
import numpy as np

class Plot():
    
    def __init__(self, problem, mesh, deck):
        field = mesh.global_fields
        # import pdb; pdb.set_trace()
        self.deck = deck
        self.nsteps =  int(problem.SimulationParameters["Number of Steps"])
        self.timestep = float(problem.SimulationParameters["Step Time"])
        self.nintervals = int(self.deck.doc["Plot"]["plot interval"])
        self.mesh = mesh
        # fields ={}
        # for aux in mesh.fields:
        #     fields[aux.name]= aux.value
        self.T = field["Temperature"]
        self.set_plots()



# -------------- BEGIN NEW PLOT GENERATION---------- 
    def set_plots(self): 
    
        self.mfig=[]
        # import pdb; pdb.set_trace()
        for i in range (0,self.nsteps,self.nintervals):
            self.mfig.append(i)
        self.fignum = 0
        self.fig = plt.figure()
# -------------- END NEW PLOT GENERATION----------  

       
    def update_T(self,T):
        self.T = T
        
    def update_Dic(self,Dic):
        self.Dic = Dic
 
# -------------- BEGIN PLOTTING----------  
    def do_plots(self,m):
                plt.clf()
                self.fignum += 1
                print(m, self.fignum)
                # plt.figure( figsize=(8, 6), dpi=280)
                plt.gcf().set_size_inches(16, 8)
                plt.gcf().set_dpi(80)        
                plt.pcolormesh(self.mesh.position["X"], self.mesh.position["Y"], self.T, vmin=290, vmax=500,cmap=self.deck.doc["Plot"]["Color Map"])
                plt.colorbar()
                self.fig.suptitle('time: {:.2f}'.format( m*self.timestep), fontsize=16)
                plt.savefig(self.deck.plot_dirTemp+self.deck.doc["Plot"]["figure temperature name"]+ str("%03d" %self.fignum) + '.jpg')

             

# -------------- END PLOTTING----------                        
                
                
                
                
                
                
                
                
        
    def do_animation(self):   
        frames = []
        # imgs = glob.glob("./output/*.jpg")
        imgs = glob.glob(self.deck.plot_dirTemp + '*.jpg')
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)
            print(i)
            
        direction=(self.deck.plot_dirTemp+self.deck.doc["Animation"]["Temperature name"]+'.gif')
        frames[0].save(direction, format='GIF',
                        append_images=frames[1:],
                        save_all=True,
                        duration=400, loop=0)       
    
    
        frames = []
        # imgs = glob.glob("./output/*.jpg")
        imgs = glob.glob(self.deck.plot_dirDic + '*.jpg')
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)
            print(i)
            
        direction=(self.deck.plot_dirDic+self.deck.doc["Animation"]["Dic name"]+'.gif')
        frames[0].save(direction, format='GIF',
                        append_images=frames[1:],
                        save_all=True,
                        duration=400, loop=0)      