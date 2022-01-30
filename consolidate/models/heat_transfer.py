import numpy as np

class HeatTransfer:

    def __init__(self, global_mesh, problem):
        # fields ={}
        # for aux in mesh.fields:
        #     fields[aux.name]= aux.value
            # import pdb; pdb.set_trace()
            
        self.dx = global_mesh.fields["increments"]["dx"]
        self.dy = global_mesh.fields["increments"]["dy"]
        self.dx2 = self.dx*self.dx
        self.dy2 = self.dy*self.dy
        
        self.dt = float(problem.SimulationParameters["Step Time"])

        self.rho = global_mesh.fields["Density"]
        self.cp = global_mesh.fields["Thermal"]["Cp"]
        self.kx = global_mesh.fields["Thermal"]["kx"]
        self.ky = global_mesh.fields["Thermal"]["ky"]
        
        self.A = global_mesh.fields["Viscosity"]["A"]
        self.Ea = global_mesh.fields["Viscosity"]["Ea"]
        self.Tg = global_mesh.fields["Viscosity"]["Tg"]
        
        self.Q = global_mesh.fields["Power Input Heat"]
        # self.h = fields ["Convection Coefficient"]
        # self.Text = fields["Interface Temperature"]

        self.calc_diffusivity(self.kx, self.ky, self.rho, self.cp)
        self.calc_w(self.diffx, self.diffy, self.dx2, self.dy2)
        self.calc_disc(self.ky)


    def calc_diffusivity(self, kx, ky, rho, cp):

        self.diffy = ky/(rho*cp)
        self.diffx = kx/(rho*cp)

    def calc_w(self, diffx,diffy,dx2,dy2):

        self.wy = diffy/dy2
        self.wx = diffx/dx2


    def calc_disc(self, ky):
        k=[]
        disc=[]
        for i in range (1, np.shape(ky)[0]-2):
            if self.ky[i, 1] != ky[i+1, 1]:
                k.append( self.ky[i,1]/ky[i+1, 1])
                disc.append(i+1)

        gamma =[]
        for i in range (0, np.size(disc)):
            gamma.append((k[i]-1)/(k[i]+1))

        self.gamma = gamma
        self.disc = disc
        self.k = k


    def do_timestep_cond_conv(self, uu,uuold, Tinter):

        # import pdb; pdb.set_trace()
        # uu[0,1:-1] = 2*self.Text[0,1:-1] - uuold[1,1:-1]
        # uu[-1,1:-1] = 2*self.Text[-1,1:-1] - uuold[-2,1:-1]
        # uu[1:-1,0] = 2*self.Text[1:-1,0] - uuold[1:-1,1]
        # uu[1:-1,-1] = 2*self.Text[1:-1,-1] - uuold[1:-1,-2]



        if not self.disc:
            uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + self.dt*(self.wy[0:-1, 0:-1])*(uuold[2:, 1:-1]-2*uuold[1:-1, 1:-1] + uuold[:-2,1:-1]) + self.dt*(self.wx[0:-1, 0:-1])*(uuold[1:-1, 2:]-2*uuold[1:-1, 1:-1] + uuold[1:-1, :-2]) + self.dt*self.Q[1:-1, 1:-1]/(self.rho[1:-1, 0:-1]*self.cp[0:-1, 0:-1])
        else:
            for i in range (0, np.size(self.disc)):
                # calculating the temperature at the discontinuity
                # firt order (can be desabled) - Accuracy 2
                # uu[self.disc[i], 1:-1] = (self.ky[self.disc[i]+1, :-1] * uuold[self.disc[i]+1, 1:-1]/self.dy[self.disc[i]+1, :-1] + self.ky[self.disc[i]-1, :-1] * uuold[self.disc[i]-1, 1:-1]/self.dy[self.disc[i]-1, :-1]) / (self.ky[self.disc[i]-1, :-1]/self.dy[self.disc[i]-1, :-1] + self.ky[self.disc[i]+1, :-1]/self.dy[self.disc[i]+1, :-1])
                # second order (better accuracty than first order) - Accuracy 4
                uu[self.disc[i], 1:-1] = 2/3 * (self.ky[self.disc[i]-1, :-1]/self.dy[self.disc[i]-1, :-1]*(2*uuold[self.disc[i]-1, 1:-1] - 1/2*uuold[self.disc[i]-2, 1:-1]) + self.ky[self.disc[i]+1, :-1]/self.dy[self.disc[i]+1, :-1]*(2*uuold[self.disc[i]+1, 1:-1] - 1/2*uuold[self.disc[i]+2, 1:-1]))/((self.ky[self.disc[i]-1, 0:-1]/self.dy[self.disc[i]-1, 0:-1])+ (self.ky[self.disc[i]+1, 0:-1]/self.dy[self.disc[i]+1, 0:-1]))
                if i < np.size(self.disc)-1:
                    # calculating for the inner domains
                    # first order - Accuracy 2
                    uu[self.disc[i]+1: self.disc[i+1], 1:-1] = uuold[self.disc[i]+1: self.disc[i+1], 1:-1] + self.dt*(self.diffy[self.disc[i]+1: self.disc[i+1], :-1]/self.dy2[self.disc[i]+1: self.disc[i+1], :-1] )*(uuold[self.disc[i]+2: self.disc[i+1]+1, 1:-1] -2*uuold[self.disc[i]+1: self.disc[i+1], 1:-1] + uuold[self.disc[i]: self.disc[i+1]-1, 1:-1]) + self.dt*(self.wx[self.disc[i]+1: self.disc[i+1], 0:-1])*(uuold[self.disc[i]+1: self.disc[i+1], 2:]-2*uuold[self.disc[i]+1: self.disc[i+1], 1:-1] + uuold[self.disc[i]+1: self.disc[i+1], :-2]) + self.dt*self.Q[self.disc[i]+1: self.disc[i+1], 1:-1] /(self.rho[self.disc[i]+1: self.disc[i+1], :-1] *self.cp[self.disc[i]+1: self.disc[i+1], :-1] )
                    # second order (better accuracy) - Accuracy 4
                    uu[self.disc[i]+2: self.disc[i+1]-1, 1:-1] = uuold[self.disc[i]+2: self.disc[i+1]-1, 1:-1] + self.dt*(self.diffy[self.disc[i]+2: self.disc[i+1]-1, :-1]/self.dy2[self.disc[i]+2: self.disc[i+1]-1, :-1] )*(-1/12*uuold[self.disc[i]: self.disc[i+1]-3, 1:-1] +4/3*uuold[self.disc[i]+1: self.disc[i+1]-2, 1:-1] -5/2* uuold[self.disc[i]+2: self.disc[i+1]-1, 1:-1] +4/3*uuold[self.disc[i]+3: self.disc[i+1], 1:-1] -1/12*uuold[self.disc[i]+4: self.disc[i+1]+1, 1:-1]  ) + self.dt*(self.wx[self.disc[i]+2: self.disc[i+1]-1, :-1])*(uuold[self.disc[i]+2: self.disc[i+1]-1, 2:]-2*uuold[self.disc[i]+2: self.disc[i+1]-1, 1:-1] + uuold[self.disc[i]+2: self.disc[i+1]-1, :-2]) + self.dt*self.Q[self.disc[i]+2: self.disc[i+1]-1, 1:-1] /(self.rho[self.disc[i]+2: self.disc[i+1]-1, :-1] *self.cp[self.disc[i]+2: self.disc[i+1]-1, :-1] )

                if i==0:
                    # calculating the temperature within the FIRST DOMAIN
                    # first order - Accuracy 2
                    uu[1:self.disc[i],1:-1] = uuold[1:self.disc[i],1:-1] + self.dt*(self.diffy[:self.disc[i]-1, 0:-1]/self.dy2[:self.disc[i]-1, 0:-1])*(uuold[2:self.disc[i]+1 ,1:-1] -2*uuold[1:self.disc[i],1:-1] + uuold[0:self.disc[i]-1,1:-1]) + self.dt*(self.wx[:self.disc[i]-1, :-1])*(uuold[1:self.disc[i],2:] -2*uuold[1:self.disc[i],1:-1] + uuold[1:self.disc[i],:-2]) + self.dt*self.Q[1:self.disc[i],1:-1]/(self.rho[1:self.disc[i], :-1]*self.cp[1:self.disc[i], :-1])
                    # second order (better accuracy) - Accuracy 4
                    uu[2:self.disc[i],1:-1] = uuold[2:self.disc[i],1:-1] + self.dt*(self.diffy[2:self.disc[i],:-1] /self.dy2[2:self.disc[i],:-1]  )*(-1/12*uuold[:self.disc[i]-2,1:-1] +4/3*uuold[1:self.disc[i]-1,1:-1] -5/2* uuold[2:self.disc[i],1:-1] +4/3*uuold[3:self.disc[i]+1,1:-1] -1/12*uuold[4:self.disc[i]+2,1:-1]) + self.dt*(self.wx[2:self.disc[i], :-1])*(uuold[2:self.disc[i], 2:] -2*uuold[2:self.disc[i], 1:-1] + uuold[2:self.disc[i], :-2]) + self.dt*self.Q[2:self.disc[i],1:-1]/(self.rho[2:self.disc[i], :-1]*self.cp[2:self.disc[i], :-1])

                if i == np.size(self.disc) -1:
                    # calculating the temperature within the LAST domain
                    # fir order - Accuracy 2
                    uu[self.disc[i] +1:-1, 1:-1] = uuold[self.disc[i] +1:-1, 1:-1] + self.dt*(self.diffy[self.disc[i]+1: , :-1]/self.dy2[self.disc[i]+1: , :-1])*(uuold[self.disc[i] +2 :, 1:-1] -2*uuold[self.disc[i] +1:-1, 1:-1] + uuold[self.disc[i]:-2, 1:-1]) + self.dt*(self.wx[self.disc[i]+1:, :-1])*(uuold[self.disc[i] +1:-1, 2:] -2*uuold[self.disc[i] +1:-1, 1:-1] + uuold[self.disc[i] +1:-1, :-2]) + self.dt*self.Q[self.disc[i] +1:-1, 1:-1]/(self.rho[self.disc[i] +1:, :-1]*self.cp[self.disc[i] +1:, :-1])
                    # second order (better accuracy) - Accuracy 4
                    uu[self.disc[i] +1:-2, 1:-1] = uuold[self.disc[i] +1:-2, 1:-1]+ self.dt*(self.diffy[self.disc[i] +1:-1, :-1] /self.dy2[self.disc[i] +1:-1, :-1]  )*(-1/12*uuold[self.disc[i] -1:-4, 1:-1] +4/3*uuold[self.disc[i]:-3, 1:-1] -5/2* uuold[self.disc[i] +1:-2, 1:-1] +4/3*uuold[self.disc[i] + 2:-1, 1:-1] -1/12*uuold[self.disc[i] +3:, 1:-1]  ) + self.dt*(self.wx[self.disc[i] +1:-1, :-1])*(uuold[self.disc[i] +1:-2, 2:]-2*uuold[self.disc[i] +1:-2, 1:-1] + uuold[self.disc[i] +1:-2, :-2]) + self.dt*self.Q[self.disc[i] +1:-2, 1:-1]/(self.rho[self.disc[i] +1:-1, :-1]*self.cp[self.disc[i] +1:-1, :-1])

        uu_inter = (uu[0,:-1] + uu[0, 1:] + uu[1, :-1] + uu[1,1:])/4

        return uu, uu_inter



    def do_timestep_viscosity(self, uu):
        eta = self.A * np.exp(self.Ea/uu)
        return eta



