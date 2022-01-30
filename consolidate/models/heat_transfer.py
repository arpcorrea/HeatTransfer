import numpy as np

class HeatTransfer:

    def __init__(self, mesh, problem):
        # import pdb; pdb.set_trace()
        fields = mesh.global_fields
        # fields ={}
        # for aux in mesh.fields:
        #     fields[aux.name]= aux.value
            # import pdb; pdb.set_trace()
            
        self.dx = fields["increments"]["dx"]
        self.dy = fields["increments"]["dy"]
        self.dx2 = self.dx*self.dx
        self.dy2 = self.dy*self.dy
        
        self.dt = float(problem.SimulationParameters["Step Time"])

        self.rho = fields["Density"]
        self.cp = fields["Cp"]
        self.kx = fields["kx"]
        self.ky = fields["ky"]
        
        self.A = fields["Viscosity"]["A"]
        self.Ea = fields["Viscosity"]["Ea"]
        # self.Tg = ["Viscosity"]["Tg"]
        
        self.Q = fields["Internal Heat Generation"]
        # self.h = fields ["Convection Coefficient"]
        # self.Text = fields["Interface Temperature"]

        self.calc_diffusivity(self.kx, self.ky, self.rho, self.cp)
        self.calc_w(self.diffx, self.diffy, self.dx2, self.dy2)


    def calc_diffusivity(self, kx, ky, rho, cp):

        self.diffy = ky/(rho*cp)
        self.diffx = kx/(rho*cp)

    def calc_w(self, diffx,diffy,dx2,dy2):

        self.wy = diffy/dy2
        self.wx = diffx/dx2



    def do_timestep_cond_conv(self, uu,uuold, mesh):
        
        # import pdb; pdb.set_trace()

        # import pdb; pdb.set_trace()
        # uu[0,1:-1] = 2*self.Text[0,1:-1] - uuold[1,1:-1]
        # uu[-1,1:-1] = 2*self.Text[-1,1:-1] - uuold[-2,1:-1]
        # uu[1:-1,0] = 2*self.Text[1:-1,0] - uuold[1:-1,1]
        # uu[1:-1,-1] = 2*self.Text[1:-1,-1] - uuold[1:-1,-2]
        
        for part in mesh.parts:
            if part.dimensions[1][0]==0:
                for key in part.bc["Thermal"]["Bottom"].keys():
                    if key == "Fixed Temperature":
                        uu[0,1:-1] = part.bc["Thermal"]["Bottom"][key]["Temperature"]
                    if key == "Convection":
                        h=part.bc["Thermal"]["Bottom"][key]["HTC"]
                        Tinf = part.bc["Thermal"]["Bottom"][key]["External Temperature"]
                        uu[0,1:-1] = (2*uu[1,1:-1]+uu[0,2:]+uu[0,:-2]+(2*self.dy[0,1:-1]*h*Tinf/self.ky[0,1:-1]))/(2*((h*self.dy[0,1:-1]/self.ky[0,1:-1])+2))
            if part.dimensions[1][1]==mesh.total_thickness:
                for key in part.bc["Thermal"]["Top"].keys():
                    if key == "Fixed Temperature":
                        uu[-1,1:-1] = part.bc["Thermal"]["Top"][key]["Temperature"]
                    if key == "Convection":
                        h=part.bc["Thermal"]["Top"][key]["HTC"]
                        Tinf = part.bc["Thermal"]["Top"][key]["External Temperature"]
                        uu[-1,1:-1] = (2*uu[-2,1:-1]+uu[-1,2:]+uu[-1,:-2]+(2*self.dy[-1,1:-1]*h*Tinf/self.ky[-1,1:-1]))/(2*((h*self.dy[-1,1:-1]/self.ky[-1,1:-1])+2))
            for key in part.bc["Thermal"]["Right"].keys():
                if key == "Fixed Temperature":
                    uu[part.nodes[1][0]+1:part.nodes[1][1]-1,0] = part.bc["Thermal"]["Right"][key]["Temperature"]
                if key == "Convection":
                   h=part.bc["Thermal"]["Right"][key]["HTC"]
                   Tinf = part.bc["Thermal"]["Right"][key]["External Temperature"]
                   # uu[part.nodes[1][0]+1:part.nodes[1][1],-1] = (2*uu[part.nodes[1][0]+1:part.nodes[1][1],-2]+uu[part.nodes[1][0]+2:part.nodes[1][1]+1,-1]+uu[part.nodes[1][0]:part.nodes[1][1]-1,-1]+(2*self.dx[part.nodes[1][0]+1:part.nodes[1][1],-1]*h*Tinf/self.kx[part.nodes[1][0]+1:part.nodes[1][1],-1]))/(2*((h*self.dx[part.nodes[1][0]+1:part.nodes[1][1],-1]/self.kx[part.nodes[1][0]+1:part.nodes[1][1],-1])+2))
                   uu[part.nodes[1][0]+1:part.nodes[1][1],-1] = (self.kx[part.nodes[1][0]+1:part.nodes[1][1],-1]*self.dy[part.nodes[1][0]+1:part.nodes[1][1],-1]*(uuold[part.nodes[1][0]+1:part.nodes[1][1],1]-uuold[part.nodes[1][0]+1:part.nodes[1][1],-1])/self.dx[part.nodes[1][0]+1:part.nodes[1][1],-1] + self.ky[part.nodes[1][0]+1:part.nodes[1][1],-1]*(self.dx[part.nodes[1][0]+1:part.nodes[1][1],-1]/2)*(uuold[part.nodes[1][0]+2:part.nodes[1][1]+1,-1]-uuold[part.nodes[1][0]+1:part.nodes[1][1],-1])/self.dy[2,-1] + self.ky[part.nodes[1][0]+1:part.nodes[1][1],-1]*(self.dx[part.nodes[1][0]+1:part.nodes[1][1],-1]/2)*(uuold[part.nodes[1][0]:part.nodes[1][1]-1,-1]-uuold[part.nodes[1][0]+1:part.nodes[1][1],-1])/self.dy[part.nodes[1][0]+1:part.nodes[1][1],-1] + h*self.dy[part.nodes[1][0]+1:part.nodes[1][1],-1]*(Tinf-uuold[part.nodes[1][0]+1:part.nodes[1][1],-1]) + (uuold[part.nodes[1][0]+1:part.nodes[1][1],-1]*self.rho[part.nodes[1][0]+1:part.nodes[1][1], -1]*self.cp[part.nodes[1][0]+1:part.nodes[1][1],-1]*(self.dx[part.nodes[1][0]+1:part.nodes[1][1],-1]/2)*self.dy[part.nodes[1][0]+1:part.nodes[1][1],-1]/self.dt))/(self.rho[part.nodes[1][0]+1:part.nodes[1][1],-1]*self.cp[part.nodes[1][0]+1:part.nodes[1][1],-1]*(self.dx[part.nodes[1][0]+1:part.nodes[1][1],-1]/2)*self.dy[part.nodes[1][0]+1:part.nodes[1][1],-1]/self.dt)
            for key in part.bc["Thermal"]["Left"].keys():
                if key == "Fixed Temperature":
                    uu[part.nodes[1][0]+1:part.nodes[1][1]-1,0] = part.bc["Thermal"]["Left"][key]["Temperature"]
                if key == "Convection":
                   h=part.bc["Thermal"]["Left"][key]["HTC"]
                   Tinf = part.bc["Thermal"]["Left"][key]["External Temperature"]
                   # uu[part.nodes[1][0]+1:part.nodes[1][1],0] = (2*uuold[part.nodes[1][0]+1:part.nodes[1][1],1]+uuold[part.nodes[1][0]+2:part.nodes[1][1]+1,0]+uuold[part.nodes[1][0]:part.nodes[1][1]-1,0]+(2*self.dx[part.nodes[1][0]+1:part.nodes[1][1],0]*h*Tinf/self.kx[part.nodes[1][0]+1:part.nodes[1][1],0]))/(2*((h*self.dx[part.nodes[1][0]+1:part.nodes[1][1],0]/self.kx[part.nodes[1][0]+1:part.nodes[1][1],0])+2))
                   uu[part.nodes[1][0]+1:part.nodes[1][1],0] = (self.kx[part.nodes[1][0]+1:part.nodes[1][1],0]*self.dy[part.nodes[1][0]+1:part.nodes[1][1],0]*(uuold[part.nodes[1][0]+1:part.nodes[1][1],1]-uuold[part.nodes[1][0]+1:part.nodes[1][1],0])/self.dx[part.nodes[1][0]+1:part.nodes[1][1],0] + self.ky[part.nodes[1][0]+1:part.nodes[1][1],0]*(self.dx[part.nodes[1][0]+1:part.nodes[1][1],0]/2)*(uuold[part.nodes[1][0]+2:part.nodes[1][1]+1,0]-uuold[part.nodes[1][0]+1:part.nodes[1][1],0])/self.dy[2,0] + self.ky[part.nodes[1][0]+1:part.nodes[1][1],0]*(self.dx[part.nodes[1][0]+1:part.nodes[1][1],0]/2)*(uuold[part.nodes[1][0]:part.nodes[1][1]-1,0]-uuold[part.nodes[1][0]+1:part.nodes[1][1],0])/self.dy[part.nodes[1][0]+1:part.nodes[1][1],0] + h*self.dy[part.nodes[1][0]+1:part.nodes[1][1],0]*(Tinf-uuold[part.nodes[1][0]+1:part.nodes[1][1],0]) + (uuold[part.nodes[1][0]+1:part.nodes[1][1],0]*self.rho[part.nodes[1][0]+1:part.nodes[1][1], 0]*self.cp[part.nodes[1][0]+1:part.nodes[1][1], 0]*(self.dx[part.nodes[1][0]+1:part.nodes[1][1],0]/2)*self.dy[part.nodes[1][0]+1:part.nodes[1][1],0]/self.dt))/(self.rho[part.nodes[1][0]+1:part.nodes[1][1], 0]*self.cp[part.nodes[1][0]+1:part.nodes[1][1], 0]*(self.dx[part.nodes[1][0]+1:part.nodes[1][1],0]/2)*self.dy[part.nodes[1][0]+1:part.nodes[1][1],0]/self.dt)

        # import pdb; pdb.set_trace()
        
        uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + self.dt*(self.wy[1:-1, 1:-1])*(uuold[2:, 1:-1]-2*uuold[1:-1, 1:-1] + uuold[:-2,1:-1]) + self.dt*(self.wx[1:-1, 1:-1])*(uuold[1:-1, 2:]-2*uuold[1:-1, 1:-1] + uuold[1:-1, :-2]) + self.dt*self.Q[1:-1, 1:-1]/(self.rho[1:-1, 1:-1]*self.cp[1:-1, 1:-1])

        return uu



    def do_timestep_viscosity(self, uu):
        eta = self.A * np.exp(self.Ea/uu)
        return eta



