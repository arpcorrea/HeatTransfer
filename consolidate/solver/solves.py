# -*- coding: utf-8 -*-
import numpy as np



class SolvesTwoPlates:
    
    def __init__(self, problem,model_HT,mesh,plots):
        self.plots = plots
        Told = mesh.fields["Temperature"].copy()
        self.Tnew = mesh.fields["Temperature"].copy()
        self.do_solver(problem, model_HT,mesh, Told)
        
    def do_solver(self,problem, model_HT,mesh, Told):
        # import pdb; pdb.set_trace()
        ViscNew = np.zeros((np.shape(self.Tnew)[0]+1, np.shape(self.Tnew)[1]+1))
        Tinter = np.zeros((np.shape(self.Tnew)[0]-1, np.shape(self.Tnew)[1]-1))
        for m in range(int(problem.SimulationParameters["Number of Steps"])):

            self.Tnew, Tinter = model_HT.do_timestep_cond_conv( self.Tnew.copy(), Told.copy(), Tinter)
            Told = self.Tnew.copy()
            self.ViscNew = model_HT.do_timestep_viscosity( Tinter)
            if m in self.plots.mfig:
                self.plots.update_T(self.Tnew)
                self.plots.do_plots(m)

            # self.dir_Visc.value = model_visc.do_timestep(self.dir_Visc.value, self.dir_T.value)

# # -------------- CALCULATE VISCOSITY FOR EACH STEP INCREMENT----------             
#             self.meshes.Visc=self.model_IC.viscosity_timestep(self.meshes.Visc, self.meshes.T)
# # -------------- CALCULATE Dic FOR EACH STEP INCREMENT----------             
#             self.meshes.Dic=self.model_IC.dic_timestep(self.meshes.Dic, self.meshes.Dic0, self.meshes.Visc, float(self.deck.doc["Simulation"]["Time Step"]))
# # -------------- UPDATE THE INTEGRAL----------             
#             self.model_IC.aux=self.model_IC.update_aux( float(self.deck.doc["Simulation"]["Time Step"]), self.meshes.Visc)
# # -------------- UPDATE Dic----------             
#             self.meshes.Dic=np.clip(self.meshes.Dic,0,1)
# # -------------- DO PLOT ACCORDING TO THE SELECTED INTERVAL----------             
#             if m in self.plots.mfig:
#                 self.plots.update_Dic(self.meshes.Dic)
#                 self.plots.update_T(self.meshes.T)       
#                 self.plots.do_plots(m)    
#         self.plots.do_animation()
#         self.model_IC.calculate_average_dic()
            